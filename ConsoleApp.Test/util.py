import json
from pathlib import Path
from typing import Any, TypeVar, Type, Optional, Union

from dacite import from_dict

T = TypeVar("T")


class Util:

    @classmethod
    def dump_json(cls, obj: Any, path: Path, indent=4):
        with open(str(path), "w") as f:
            json.dump(obj, f, indent=indent)

    @classmethod
    def load_json(cls, path: Path) -> Any:
        # noinspection PyBroadException
        try:
            with open(str(path)) as f:
                report = json.load(f)
            return report
        except:
            return None

    @classmethod
    def load_json_as_dataclass(cls, path: Union[Path, str], data_class: Type[T]) -> Optional[T]:
        # noinspection PyBroadException
        try:
            with open(str(path), "r") as f:
                json_dict = json.load(f)
                obj = from_dict(data_class=data_class, data=json_dict)
                return obj
        except Exception:
            return None


class UtilPath:
    default_config_path: Path = Path(__file__).resolve().parent / "cases.yml"
    cases_path: Path = Path("cases") / "cases.txt"
    result_dir: Path = Path(__file__).resolve().parent / "result"
    result_junit_xml_path: Path = result_dir / "result.xml"

    @classmethod
    def case_result_dir(cls, case_name: str) -> Path:
        return cls.result_dir / case_name

    @classmethod
    def case_test_report_path(cls, case_name: str) -> Path:
        return cls.case_result_dir(case_name) / "test-report.json"

    @classmethod
    def case_result_report_path(cls, case_name: str) -> Path:
        return cls.case_result_dir(case_name) / "result-report.json"
