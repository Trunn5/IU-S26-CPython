import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.LongSupplier;

public class Benchmarks {
    private static volatile long sink = 0L;
    private static long fibonacciIter(int n) {
        final long mod = 1_000_000_007L;
        long a = 0;
        long b = 1;
        for (int i = 0; i < n; i++) {
            long next = (a + b) % mod;
            a = b;
            b = next;
        }
        return a;
    }

    private static int primeCount(int limit) {
        if (limit < 2) {
            return 0;
        }
        int count = 0;
        for (int n = 2; n <= limit; n++) {
            boolean isPrime = true;
            int root = (int) Math.sqrt(n);
            for (int d = 2; d <= root; d++) {
                if (n % d == 0) {
                    isPrime = false;
                    break;
                }
            }
            if (isPrime) {
                count++;
            }
        }
        return count;
    }

    private static int matrixMul(int size) {
        int[][] a = new int[size][size];
        int[][] b = new int[size][size];
        int[][] c = new int[size][size];
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                a[i][j] = (i + j) % 10;
                b[i][j] = (i * j) % 7;
            }
        }
        for (int i = 0; i < size; i++) {
            for (int k = 0; k < size; k++) {
                int aik = a[i][k];
                for (int j = 0; j < size; j++) {
                    c[i][j] += aik * b[k][j];
                }
            }
        }
        return c[0][0];
    }

    private static int jsonRoundtrip(int items) {
        // Deliberately manual JSON encode/decode to avoid external dependencies.
        StringBuilder sb = new StringBuilder();
        sb.append("[");
        for (int i = 0; i < items; i++) {
            sb.append("{\"id\":").append(i)
              .append(",\"name\":\"user_").append(i)
              .append("\",\"active\":").append(i % 2 == 0 ? "true" : "false")
              .append(",\"score\":").append(i * 1.5)
              .append(",\"tags\":[\"tag_").append(i % 10).append("\",\"group_").append(i % 5).append("\"]}");
            if (i + 1 < items) {
                sb.append(",");
            }
        }
        sb.append("]");
        String encoded = sb.toString();
        int count = 0;
        for (int i = 0; i < encoded.length(); i++) {
            if (encoded.charAt(i) == '{') {
                count++;
            }
        }
        return count;
    }

    private static LongSupplier benchmarkByName(String name) {
        return switch (name) {
            case "fibonacci_iter" -> () -> fibonacciIter(180_000);
            case "prime_count" -> () -> primeCount(20_000);
            case "matrix_mul" -> () -> matrixMul(120);
            case "json_roundtrip" -> () -> jsonRoundtrip(20_000);
            default -> null;
        };
    }

    private static String getArg(String[] args, String key, String defaultValue) {
        for (int i = 0; i < args.length - 1; i++) {
            if (args[i].equals("--" + key)) {
                return args[i + 1];
            }
        }
        return defaultValue;
    }

    public static void main(String[] args) {
        String benchmark = getArg(args, "benchmark", null);
        int warmup = Integer.parseInt(getArg(args, "warmup", "5"));
        int repeat = Integer.parseInt(getArg(args, "repeat", "7"));

        if (benchmark == null) {
            throw new IllegalArgumentException("Missing --benchmark");
        }

        LongSupplier fn = benchmarkByName(benchmark);
        if (fn == null) {
            throw new IllegalArgumentException("Unknown benchmark: " + benchmark);
        }

        for (int i = 0; i < warmup; i++) {
            sink ^= fn.getAsLong();
        }

        List<Double> times = new ArrayList<>();
        List<Double> memories = new ArrayList<>();
        Runtime runtime = Runtime.getRuntime();

        for (int i = 0; i < repeat; i++) {
            System.gc();
            long beforeMem = runtime.totalMemory() - runtime.freeMemory();
            long start = System.nanoTime();
            sink ^= fn.getAsLong();
            long elapsed = System.nanoTime() - start;
            long afterMem = runtime.totalMemory() - runtime.freeMemory();
            times.add(elapsed / 1_000_000.0);
            memories.add((afterMem - beforeMem) / 1024.0);
        }

        double avgTime = times.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
        double avgMemory = memories.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);

        Map<String, Object> out = new HashMap<>();
        out.put("benchmark", benchmark);
        out.put("time_ms", avgTime);
        out.put("memory_kb", avgMemory);
        out.put("sink", sink);

        System.out.println(
                "{\"benchmark\":\"" + out.get("benchmark")
                        + "\",\"time_ms\":" + out.get("time_ms")
                        + ",\"memory_kb\":" + out.get("memory_kb")
                        + ",\"sink\":" + out.get("sink")
                        + "}");
    }
}
