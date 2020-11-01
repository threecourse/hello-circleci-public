using System;
using Newtonsoft.Json;

namespace ConsoleApp
{
    /// <summary>
    /// 入力情報
    /// </summary>
    [JsonObject]
    class Input
    {
        [JsonProperty("x")] public int x { get; set; }
        [JsonProperty("y")] public int y { get; set; }
    }

    /// <summary>
    /// プログラムによる計算のレポート
    /// </summary>
    [JsonObject]
    class ResultReport
    {
        [JsonProperty("status")] public string Status { get; set; }

        [JsonProperty("start_time")] public DateTime StartTime { get; set; }

        [JsonProperty("execution_time_seconds")]
        public double ExecutionTimeSeconds { get; set; }

        [JsonProperty("summary")] public ResultSummary Summary { get; set; }
        [JsonProperty("failure")] public ResultFailure Failure { get; set; }
    }

    /// <summary>
    /// プログラムによる計算結果のサマリー
    /// </summary>
    [JsonObject]
    class ResultSummary
    {
        [JsonProperty("answer")] public int Answer { get; set; }
    }

    /// <summary>
    /// プログラムによる計算のエラー情報
    /// </summary>
    [JsonObject]
    class ResultFailure
    {
        [JsonProperty("type")] public string Type;
        [JsonProperty("message")] public string Message;
        [JsonProperty("message_detail")] public string MessageDetail;
    }
}