# Bra-Ket Dataset Generation Guide

## Quick Start

```python
from generate_braket_dataset import BraKetDatasetGenerator

# Training data (uses symbols: ψ,φ,χ,a,b,c,0,1)
train_gen = BraKetDatasetGenerator(use_training_symbols=True)
train_data = train_gen.generate_dataset(n_samples=100000)

# Probe data (uses symbols: x,y,z,p,q,r,m,n)
probe_gen = BraKetDatasetGenerator(use_training_symbols=False)
probe_data = probe_gen.generate_dataset(n_samples=10000)
```

## What the Generator Creates

### Expression Types & Their Purpose

1. **Linearity (25%)**: `⟨ψ|(3|φ⟩ + 2i|χ⟩) = 3⟨ψ|φ⟩ + 2i⟨ψ|χ⟩`
   - Tests: Distributive property of inner products
   - Key learning: Linear combinations distribute

2. **Conjugation (15%)**: `⟨a|b⟩ = 2+i, ⟨b|a⟩ = 2-i`
   - Tests: Hermitian conjugation rule
   - Key learning: Complex conjugation (i → -i)

3. **Ket Conjugation (10%)**: `(3-2i|ψ⟩)† = 3+2i⟨ψ|`
   - Tests: Adjoint operation on kets
   - Key learning: Conjugate coefficients when taking adjoint

4. **Orthonormal Relations (20%)**: `⟨0|1⟩ = 0`, `⟨ψ|ψ⟩ = 1`
   - Tests: Basis properties
   - Key learning: Orthogonality and normalization

5. **Norm Expressions (10%)**: `(3+i|ψ⟩)†(3+i|ψ⟩) = 10⟨ψ|ψ⟩`
   - Tests: |α|² calculation
   - Key learning: Magnitude of complex coefficients

6. **Both-Side Distribution (10%)**: `(⟨ψ| + ⟨φ|)|χ⟩ = ⟨ψ|χ⟩ + ⟨φ|χ⟩`
   - Tests: Linearity in first argument
   - Key learning: Bras also distribute

7. **Multi-Term (5%)**: `⟨ψ|(α|φ⟩ + β|χ⟩ + γ|ω⟩) = ...`
   - Tests: Complex distributive chains
   - Key learning: Generalization to many terms

8. **Concrete Evaluation (5%)**: `⟨ψ|φ⟩ = 2, ⟨ψ|χ⟩ = 3i. ⟨ψ|(|φ⟩ + |χ⟩) = 2+3i`
   - Tests: Multi-step reasoning
   - Key learning: Combining known facts

## Key Features

### Symbol Separation
- **Training symbols**: {ψ, φ, χ, a, b, c, 0, 1}
- **Probe symbols**: {x, y, z, p, q, r, m, n}
- **Critical**: Zero overlap ensures testing generalization, not memorization

### Complex Number Handling
- Real coefficients: `3`, `-5`, `0`
- Pure imaginary: `i`, `-4i`, `2i`
- Complex: `2+3i`, `-1-5i`, `0.5+0.8i`
- Automatic conjugation: `3+2i → 3-2i`

### Expression Validity
All generated expressions are mathematically correct:
- Proper bracket matching
- Consistent conjugation rules
- Valid coefficient arithmetic
- Correct distributive expansions

## Customization

### Adjust Distribution
```python
custom_dist = {
    'linearity': 0.40,        # More linearity examples
    'conjugation': 0.20,      # More conjugation
    'orthonormal': 0.15,      # Less orthonormal
    'norm': 0.05,
    'distributive_both': 0.05,
    'multi_term': 0.10,
    'concrete_eval': 0.05
}

gen = BraKetDatasetGenerator()
data = gen.generate_dataset(n_samples=50000, distribution=custom_dist)
```

### Custom Symbols
```python
gen = BraKetDatasetGenerator(
    training_symbols={'α', 'β', 'γ', 'δ', '↑', '↓'},
    probe_symbols={'u', 'v', 'w', 'η', 'ξ'}
)
```

### Coefficient Range
Modify `random_coefficient()` to control value ranges:
```python
# In the class method:
def random_coefficient(self, allow_complex=True, max_val=5):  # Smaller values
    real = random.randint(-max_val, max_val)
    ...
```

## Usage for Transformer Training

### 1. Tokenization Strategy

**Option A: Character-level** (simplest)
```python
vocab = set('⟨⟩|()†+=0123456789i-ψφχabc ')
# Each character is a token
```

**Option B: Symbol-level** (recommended)
```python
vocab = ['⟨', '⟩', '|', '(', ')', '†', '=', '+', '-',
         'ψ', 'φ', 'χ', 'a', 'b', 'c', '0', '1',
         '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'i']
# Each mathematical symbol is a token
```

**Option C: Subword** (most flexible)
- Use BPE/WordPiece on the generated text
- Learns optimal tokenization from data

### 2. Formatting for Next-Token Prediction

The raw expressions are already in the right format:
```
⟨ψ|(3|φ⟩ + 2|χ⟩) = 3⟨ψ|φ⟩ + 2⟨ψ|χ⟩
```

Model learns:
- Given `⟨ψ|(3|φ⟩ + 2|χ⟩) =`, predict `3`
- Given `⟨ψ|(3|φ⟩ + 2|χ⟩) = 3`, predict `⟨`
- etc.

### 3. Train/Val/Test Split

```python
# Generate datasets
train_gen = BraKetDatasetGenerator(use_training_symbols=True)
train_full = train_gen.generate_dataset(100000)

# Split training data
train_data = train_full[:90000]
val_data = train_full[90000:]

# Probe data (completely separate symbols)
probe_gen = BraKetDatasetGenerator(use_training_symbols=False)
probe_data = probe_gen.generate_dataset(10000)
```

## Next Steps

### Phase 1: Verify Data Quality
```bash
python generate_braket_dataset.py
head -100 train_braket.txt  # Inspect training data
head -100 probe_braket.txt  # Inspect probe data
```

### Phase 2: Prepare for Training
- Tokenize expressions
- Create PyTorch/JAX dataset loaders
- Set up transformer model (small: 2-4 layers, 128-256 dim)

### Phase 3: Training
- Train with next-token prediction loss
- Save checkpoints every 10K steps
- Monitor training loss convergence

### Phase 4: Probing
- Load trained model
- Test on probe_data (novel symbols)
- Measure accuracy on each expression type
- Check generalization: Did it learn abstract rules?

## Expected Outcomes

### Strong Signals of Learning
✓ >90% accuracy on probe linearity tests  
✓ >85% accuracy on probe conjugation tests  
✓ >80% accuracy on multi-step reasoning with novel symbols  

### Failure Modes to Watch
✗ High training accuracy but low probe accuracy → Memorization  
✗ Good on simple probes, fails on multi-term → Partial learning  
✗ Can't handle novel coefficient values → Overfitting to training range  

## Tips

1. **Start small**: Generate 10K samples first, verify correctness
2. **Check symbol separation**: Ensure no training symbols in probe data
3. **Monitor diversity**: Should see varied expression types
4. **Validate syntax**: All expressions should be parseable
5. **Test edge cases**: Zero coefficients, pure real/imaginary, identity operations

## Example Verification Script

```python
# Quick validation
from generate_braket_dataset import BraKetDatasetGenerator

gen = BraKetDatasetGenerator()
samples = gen.generate_dataset(1000)

# Check symbol usage
train_syms = {'ψ','φ','χ','a','b','c','0','1'}
probe_syms = {'x','y','z','p','q','r','m','n'}

for sample in samples:
    assert not any(s in sample for s in probe_syms), "Probe symbol in training!"

print("✓ All validations passed")
```
