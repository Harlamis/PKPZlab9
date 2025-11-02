using System;
using System.Collections.Generic;

namespace Task3
{
    public class ArrayStack
    {
        private int[] _items;
        private int _top;

        public ArrayStack(int maxSize)
        {
            _items = new int[maxSize];
            _top = -1;
        }

        public bool IsEmpty()
        {
            return _top == -1;
        }

        public bool IsFull()
        {
            return _top == _items.Length - 1;
        }

        public void Push(int position)
        {
            if (IsFull())
            {
                Console.WriteLine("Error: Stack overflow!");
                return;
            }

            _top++;
            _items[_top] = position;
        }

        public int Pop()
        {
            if (IsEmpty())
            {
                return -1;
            }

            int position = _items[_top];
            _top--;
            return position;
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            string expression;
            string filePath = "expression.txt";

            try
            {
                expression = File.ReadAllText(filePath);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error reading file '{filePath}': {ex.Message}");
                return;
            }

            Console.WriteLine($"Expression to check: {expression}");
            Console.WriteLine(new string('-', 30));

            var stack = new ArrayStack(expression.Length);
            var pairs = new List<(int Open, int Close)>();
            bool isBalanced = true;

            for (int i = 0; i < expression.Length; i++)
            {
                char c = expression[i];
                int position = i + 1;

                if (c == '(')
                {
                    stack.Push(position);
                }
                else if (c == ')')
                {
                    int openPosition = stack.Pop();

                    if (openPosition == -1)
                    {
                        isBalanced = false;
                        break;
                    }
                    else
                    {
                        pairs.Add((openPosition, position));
                    }
                }
            }

            if (isBalanced && stack.IsEmpty())
            {
                Console.WriteLine("Parentheses are balanced.");
                Console.WriteLine("Found pairs (opening position, closing position):");

                foreach (var pair in pairs)
                {
                    Console.WriteLine($"  (Position {pair.Open}, Position {pair.Close})");
                }
            }
            else
            {
                Console.WriteLine("Error: Parentheses are not balanced.");
            }
        }
    }
} 
