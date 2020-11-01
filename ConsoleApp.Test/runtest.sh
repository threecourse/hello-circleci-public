cd ConsoleApp.Test
python test_util.py --generate-case-list
python test_util.py --delete-result
python test_runner.py case1 case2 case3 case4
python test_util.py --aggregate-result
