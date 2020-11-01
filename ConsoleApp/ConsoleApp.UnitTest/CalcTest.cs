using System;
using Xunit;
using ConsoleApp;

namespace ConsoleApp.UnitTest
{
    public class UnitTest1
    {
        [Fact]
        public void Test1()
        {
            var calc = new Calc();
            calc.Calculate(10, 20).Is(200);
        }
        
        [Fact]
        public void Test2()
        {
            var calc = new Calc();
            calc.Calculate(100, 200).Is(20000);
        }
    }
}