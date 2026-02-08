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


