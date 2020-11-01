# Pythonスクリプトの形で実行する必要がある場合
import argparse
import subprocess
from dataclasses import asdict
from pathlib import Path
from typing import Optional, Tuple, List

from data import TestConfig, TestCase, TestReport, TestFailure, ResultReport
from test_util import Util, UtilPath


# noinspection PyMethodMayBeStatic
class Runner:
    """
    ランテストを実行し、テストレポートを作成する
    """

    def run(self, test_config_path: str, test_cases: List[str]):
        """一連のテストケースのランテストの実行を行う"""

        if test_config_path is None:
            test_config_path = UtilPath.default_config_path
        test_config = TestConfig.load(test_config_path)
        for case_name in test_cases:
            if case_name in test_config.cases_dict:
                self._run_case(test_config.cases_dict[case_name])

    def _run_case(self, test_case: TestCase):
        """あるテストケースのランテストの実行を行う"""
        # 対象フォルダ
        input_dir = Path(test_case.input_dir).absolute()
        result_dir = UtilPath.case_result_dir(test_case.name).absolute()

        # ランの実行とレポートの作成
        # パスの空白に対応している
        cmd = f"dotnet run --project ../ConsoleApp/ConsoleApp -- \"{input_dir}\" \"{result_dir}\""
        exit_code = subprocess.call(cmd, shell=True)
        if exit_code == 0:
            report = self._create_report(test_case)
        else:
            report = self._program_fail_report(test_case)

        # レポートの出力
        report_dict = asdict(report)
        Util.dump_json(report_dict, UtilPath.case_test_report_path(test_case.name))

    def _create_report(self, test_case: TestCase) -> 'TestReport':
        """プログラムが正しく動いた前提でレポートを作成する"""
        result_report_path = UtilPath.case_result_report_path(test_case.name)
        result_report = Util.load_json_as_dataclass(result_report_path, ResultReport)
        expected_path = Path(test_case.expected_path)
        expected = Util.load_json(expected_path)

        # プログラム結果レポートの読込に失敗した場合
        if result_report is None:
            report = self._result_report_load_fail_report(test_case)
            return report

        # 出力されるレポート形式は正当である前提
        if result_report.status == "success":
            # 成功のレポートがプログラムによって作成されているケース
            name = test_case.name
            start_time = result_report.start_time
            execution_time_seconds = result_report.execution_time_seconds
            actual = result_report.summary
            success, test_failure = self._assert_result_report(actual, expected)
            if success:
                status = "success"
                failure = None
            else:
                status = "failure"
                failure = test_failure
            return TestReport(
                name=name,
                start_time=start_time,
                execution_time_seconds=execution_time_seconds,
                status=status,
                failure=failure,
            )
        elif result_report.status == "failure":
            # 失敗のレポートがプログラムによって作成されているケース
            name = test_case.name
            start_time = result_report.start_time
            execution_time_seconds = result_report.execution_time_seconds
            status = "failure"
            failure = TestFailure(
                type=result_report.failure.type,
                message=result_report.failure.message,
                message_detail=result_report.failure.message_detail
            )
            return TestReport(
                name=name,
                start_time=start_time,
                execution_time_seconds=execution_time_seconds,
                status=status,
                failure=failure,
            )

    def _assert_result_report(self, actual: dict, expected: dict) -> Tuple[bool, Optional[TestFailure]]:
        """プログラム結果のレポートの値が、テストケースの予期する値と一致するかを確認する

        :returns テストが成功したかどうか、テスト失敗の出力
        """
        messages = []
        success = True
        for key, expected_value in expected.items():
            actual_value = actual.get(key, None)
            if actual_value != expected_value:
                success = False
                message = f"assertion failed - key:{key} expected:{expected_value} actual:{actual_value}"
                messages.append(message)

        failure = TestFailure(
            type="assertion failed",
            message="failed assertion",
            message_detail="\n".join(messages)
        )
        if success:
            return True, None
        else:
            return False, failure

    def _result_report_load_fail_report(self, test_case: TestCase) -> 'TestReport':
        """プログラム結果のレポートの読込に失敗した場合のレポートを作成する"""
        status = "failure"
        start_time = "NA"
        failure = TestFailure(
            type="result-report load error",
            message="cannot load result-report file",
            message_detail="",
        )
        return TestReport(
            name=test_case.name,
            start_time=start_time,
            execution_time_seconds=0.0,
            status=status,
            failure=failure)

    def _program_fail_report(self, test_case: TestCase) -> 'TestReport':
        """エラーが出た場合のレポートを作成する"""
        status = "failure"
        start_time = "NA"
        failure = TestFailure(
            type="program execution error",
            message="failed to execute program",
            message_detail="",
        )
        return TestReport(
            name=test_case.name,
            start_time=start_time,
            execution_time_seconds=0.0,
            status=status,
            failure=failure)


if __name__ == "__main__":
    # 引数`test_case`のみを受け取るとする
    parser = argparse.ArgumentParser()
    parser.add_argument('--test-config-path', type=str, default=None)
    parser.add_argument('test_cases', type=str, nargs='*')
    args = parser.parse_args()

    runner = Runner()
    runner.run(args.test_config_path, args.test_cases)
