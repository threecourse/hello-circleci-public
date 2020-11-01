using System;
using System.IO;
using System.Runtime.CompilerServices;
using Newtonsoft.Json;

[assembly: InternalsVisibleTo("ConsoleApp.UnitTest")]
namespace ConsoleApp
{
    class Program
    {
        static void Main(string[] args)
        {
            // パラメータ
            if (args.Length < 2)
                throw new Exception("directories should be designated");
            var inputDir = args[0]; // relative from CurrentDirectory
            var outputDir = args[1]; // relative from CurrentDirectory

            var inputPath = Path.Combine(inputDir, "input.json");
            var resultPath = Path.Combine(outputDir, "result-report.json");
            var reader = new StreamReader(inputPath);
            var inputJson = reader.ReadToEnd();
            reader.Close();
            var input = JsonConvert.DeserializeObject<Input>(inputJson);

            // 計算の実行
            var runner = new Runner();
            var report = runner.Run(input);

            // 出力
            string reportJson = JsonConvert.SerializeObject(report, Formatting.Indented);
            Directory.CreateDirectory(Path.GetDirectoryName(resultPath));
            var writer = new StreamWriter(resultPath);
            writer.WriteLine(reportJson);
            writer.Close();
        }
    }

    class Runner
    {
        public ResultReport Run(Input input)
        {
            var startTime = DateTime.Now; // ここでは計算開始時としている
            var calc = new Calc();
            try
            {
                var answer = calc.Calculate(input.x, input.y);
                var summary = new ResultSummary {Answer = answer};
                var endTime = DateTime.Now;
                var executionTimeSeconds = (endTime - startTime).TotalSeconds;
                var report = new ResultReport
                {
                    Status = "success",
                    StartTime = startTime,
                    ExecutionTimeSeconds = executionTimeSeconds,
                    Summary = summary,
                    Failure = null,
                };
                return report;
            }
            catch (Exception ex)
            {
                var endTime = DateTime.Now;
                var executionTimeSeconds = (endTime - startTime).TotalSeconds;
                var failure = new ResultFailure
                {
                    Message = ex.Message,
                    MessageDetail = ex.ToString(),
                    Type = ex.GetType().ToString(),
                };
                var report = new ResultReport
                {
                    Status = "failure",
                    StartTime = startTime,
                    ExecutionTimeSeconds = executionTimeSeconds,
                    Summary = null,
                    Failure = failure,
                };
                return report;
            }
        }
    }
}