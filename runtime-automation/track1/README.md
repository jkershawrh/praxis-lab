# Track 1 red/green cycle

Run validation before solving. A fresh namespace should return non-zero with JSON state `red`:

```bash
python3 runtime-automation/track1/validate.py
```

Apply the Track 1 mock deployment:

```bash
./runtime-automation/track1/solve.sh
```

Run validation again. It must return zero with JSON state `green`:

```bash
python3 runtime-automation/track1/validate.py
```

The mock credential has no value outside the lab. The RHPDS real-backend overlay uses separately provisioned model access and removes the public Route.
