import argparse
import shutil
import sys
from pathlib import Path
from typing import List

from data import TestConfig, TestReport, XMLUtil
from util import Util, UtilPath


class TestUtility:

    @classmethod
    def generate_case_list(cls, test_config_path: str):
        """CircleCIで分割実行を行うために引数のリストを出力する"""
        if test_config_path is None:
            test_config_path = UtilPath.default_config_path

        test_config = TestConfig.load(test_config_path)
        with open(str(UtilPath.cases_path), "w") as f:
            f.write("\n".join(test_config.case_names))
            f.write("\n")

    @classmethod
    def delete_result(cls):
        """resultフォルダを削除する"""
        if Path(UtilPath.result_dir).exists():
            shutil.rmtree(UtilPath.result_dir)

    @classmethod
    def aggregate_result(cls, test_config_path: str):
        """テストレポートを集計し、Junit形式のXMLファイルを出力する"""
        if test_config_path is None:
            test_config_path = UtilPath.default_config_path
        test_config = TestConfig.load(test_config_path)

        # レポートを集計する
        test_reports: List[TestReport] = []
        for case_name in test_config.case_names:
            test_report_path = UtilPath.case_test_report_path(case_name)
            test_report = Util.load_json_as_dataclass(test_report_path, TestReport)
            if test_report is None:
                # テストレポートが読み込めることを前提とする
                raise Exception
            test_reports.append(test_report)

        successes = sum([report.status == "success" for report in test_reports])
        success_all_cases = successes == len(test_reports)

        tree = XMLUtil.to_junit_xml(test_reports)
        tree.write(str(UtilPath.result_junit_xml_path), encoding="utf-8", xml_declaration=True)

        # noinspection PyPep8Naming
        FAIL_IF_HAS_FAILURE_CASE = False
        if FAIL_IF_HAS_FAILURE_CASE and not success_all_cases:
            # 失敗テストがある場合はFailさせることもできる
            exit_code = 10
            sys.exit(exit_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--test-config-path', type=str, default=None)
    parser.add_argument('--generate-case-list', action='store_true')
    parser.add_argument('--delete-result', action='store_true')
    parser.add_argument('--aggregate-result', action='store_true')
    args = parser.parse_args()

    if args.delete_result:
        TestUtility.delete_result()

    if args.generate_case_list is not None:
        TestUtility.generate_case_list(args.test_config_path)

    if args.aggregate_result:
        TestUtility.aggregate_result(args.test_config_path)
