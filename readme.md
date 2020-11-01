### テスト環境の構築

以下をCircleCI上でできる環境を構築する
* C#プログラムのユニットテスト
* C#プログラムの統合テスト（Pythonを利用してランを実行する）  

### 環境

以下でそれぞれ動くように構成した
* ローカル（.NET core SDK 3.1 + Python3.7 + Pip + Poetry）
* CircleCI
* Docker

### docker 

* ローカルでの実行  
`./ConsoleApp/unittest.sh`  
`./ConsoleApp.Test/runtest.sh`

* CircleCIでの実行  
`.circleci/config.yml` を参照

* Dockerのbuild  
`docker-compose build`

* Dockerでの実行  
`docker-compose run cspython bash tests/run.sh`  
`docker-compose run cspython bash ConsoleApp.Test/run.sh`

