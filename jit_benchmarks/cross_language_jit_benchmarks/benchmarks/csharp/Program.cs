using System.Diagnostics;
using System.Text;

static long FibonacciIter(int n)
{
    const long mod = 1_000_000_007L;
    long a = 0;
    long b = 1;
    for (int i = 0; i < n; i++)
    {
        long next = (a + b) % mod;
        a = b;
        b = next;
    }
    return a;
}

static int PrimeCount(int limit)
{
    if (limit < 2)
    {
        return 0;
    }
    int count = 0;
    for (int n = 2; n <= limit; n++)
    {
        bool isPrime = true;
        int root = (int)Math.Sqrt(n);
        for (int d = 2; d <= root; d++)
        {
            if (n % d == 0)
            {
                isPrime = false;
                break;
            }
        }
        if (isPrime)
        {
            count++;
        }
    }
    return count;
}

static int MatrixMul(int size)
{
    int[,] a = new int[size, size];
    int[,] b = new int[size, size];
    int[,] c = new int[size, size];
    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            a[i, j] = (i + j) % 10;
            b[i, j] = (i * j) % 7;
        }
    }

    for (int i = 0; i < size; i++)
    {
        for (int k = 0; k < size; k++)
        {
            int aik = a[i, k];
            for (int j = 0; j < size; j++)
            {
                c[i, j] += aik * b[k, j];
            }
        }
    }
    return c[0, 0];
}

static int JsonRoundtrip(int items)
{
    StringBuilder sb = new StringBuilder();
    sb.Append('[');
    for (int i = 0; i < items; i++)
    {
        sb.Append("{\"id\":").Append(i)
          .Append(",\"name\":\"user_").Append(i)
          .Append("\",\"active\":").Append(i % 2 == 0 ? "true" : "false")
          .Append(",\"score\":").Append(i * 1.5)
          .Append(",\"tags\":[\"tag_").Append(i % 10).Append("\",\"group_").Append(i % 5).Append("\"]}");
        if (i + 1 < items)
        {
            sb.Append(',');
        }
    }
    sb.Append(']');

    string encoded = sb.ToString();
    int count = 0;
    foreach (char ch in encoded)
    {
        if (ch == '{')
        {
            count++;
        }
    }
    return count;
}

static Func<long> BenchmarkByName(string name) => name switch
{
    "fibonacci_iter" => () => FibonacciIter(180_000),
    "prime_count" => () => PrimeCount(20_000),
    "matrix_mul" => () => MatrixMul(120),
    "json_roundtrip" => () => JsonRoundtrip(20_000),
    _ => throw new ArgumentException($"Unknown benchmark: {name}")
};

static string? ArgValue(string[] args, string name)
{
    string key = $"--{name}";
    for (int i = 0; i < args.Length - 1; i++)
    {
        if (args[i] == key)
        {
            return args[i + 1];
        }
    }
    return null;
}

string? benchmark = ArgValue(args, "benchmark");
int warmup = int.Parse(ArgValue(args, "warmup") ?? "5");
int repeat = int.Parse(ArgValue(args, "repeat") ?? "7");

if (benchmark is null)
{
    throw new ArgumentException("Missing --benchmark");
}

Func<long> fn = BenchmarkByName(benchmark);
long sink = 0;

for (int i = 0; i < warmup; i++)
{
    sink ^= fn();
}

List<double> times = new();
List<double> memories = new();

for (int i = 0; i < repeat; i++)
{
    GC.Collect();
    GC.WaitForPendingFinalizers();
    GC.Collect();

    long beforeMem = GC.GetTotalMemory(true);
    Stopwatch sw = Stopwatch.StartNew();
    sink ^= fn();
    sw.Stop();
    long afterMem = GC.GetTotalMemory(false);

    times.Add(sw.Elapsed.TotalMilliseconds);
    memories.Add((afterMem - beforeMem) / 1024.0);
}

double avgTime = times.Average();
double avgMemory = memories.Average();

Console.WriteLine($"{{\"benchmark\":\"{benchmark}\",\"time_ms\":{avgTime},\"memory_kb\":{avgMemory},\"sink\":{sink}}}");
