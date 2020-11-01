import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Union, Dict

import yaml


@dataclass
class TestConfig:
    """テストケース全体の設定"""
    case_names: List[str]
    cases_dict: Dict[str, 'TestCase']

    @classmethod
    def load(cls, path: Union[str, Path]):
        with open(str(path), "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        case_names = []
        cases_dict = {}
        for config_case in config["cases"]:
            name, input_dir = config_case["name"], config_case["input_dir"]
            assert (name not in cases_dict)
            case_names.append(name)
            cases_dict[name] = TestCase(name=name, input_dir=input_dir)

        return TestConfig(case_names=case_names, cases_dict=cases_dict)


@dataclass
class TestCase:
    """テストケース"""

    name: str
    input_dir: str

    @property
    def expected_path(self) -> str:
        return self.input_dir + "/expected.json"


@dataclass
class TestReport:
    """テストレポート"""

    name: str
    start_time: str  # 文字列として扱う
    execution_time_seconds: float
    status: str  # success/failure
    failure: Optional['TestFailure']


@dataclass
class TestFailure:
    """テストレポートの失敗の情報"""

    type: str
    message: str
    message_detail: str


@dataclass
class ResultReport:
    """プログラムによる計算のレポート"""
    status: str
    start_time: str  # 文字列として扱う
    execution_time_seconds: float
    summary: Optional[dict]
    failure: Optional['ResultFailure']


@dataclass
class ResultFailure:
    """プログラムによる計算の失敗の情報"""
    type: str
    message: str
    message_detail: str


class XMLUtil:
    """JUnit XML形式への変換"""

    @classmethod
    def to_junit_xml_element(cls, report: TestReport) -> ET.Element:

        test_case = ET.Element('testcase', {
            'name': report.name,
            'time': str(report.execution_time_seconds),
        })
        if report.status == "failure":
            failure = ET.SubElement(
                test_case, "failure",
                {
                    "type": report.failure.type,
                    "message": report.failure.message
                }
            )
            failure.text = report.failure.message_detail
        return test_case

    @classmethod
    def to_junit_xml(cls, reports: List['TestReport']) -> ET.ElementTree:
        elements: List[ET.Element] = []
        for report in reports:
            element = cls.to_junit_xml_element(report)
            elements.append(element)
        name = "test"
        errors = 0
        failures = sum([report.status == "failure" for report in reports])
        skipped = 0
        tests = len(reports)
        time = 0
        xml = ET.Element('testsuite', {
            "name": name,
            "errors": str(errors),
            "failures": str(failures),
            "skipped": str(skipped),
            "tests": str(tests),
            "time": str(time),
        })
        for element in elements:
            xml.append(element)
        tree = ET.ElementTree(xml)
        return tree
