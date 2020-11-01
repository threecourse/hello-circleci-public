using System;
using System.Runtime.CompilerServices;

namespace ConsoleApp
{
   
    class Calc
    {
        public int Calculate(int x, int y)
        {
            if (x == 999)
            {
                throw new ArgumentException("This number is not legit.");
            }
            return x * y;
        }
    }
}