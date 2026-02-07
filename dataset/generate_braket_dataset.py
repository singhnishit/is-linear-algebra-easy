"""
Bra-Ket Algebra Dataset Generator
Generates synthetic expressions for training transformers on quantum formalism
"""

import random
import numpy as np
from typing import List, Tuple, Set
from dataclasses import dataclass

@dataclass
class Complex:
    """Represent complex numbers as a+bi"""
    real: float
    imag: float
    
    def __str__(self):
        if self.imag == 0:
            return f"{self.real:.0f}" if self.real == int(self.real) else f"{self.real}"
        elif self.real == 0:
            if self.imag == 1:
                return "i"
            elif self.imag == -1:
                return "-i"
            return f"{self.imag:.0f}i" if self.imag == int(self.imag) else f"{self.imag}i"
        else:
            sign = "+" if self.imag > 0 else ""
            imag_str = "i" if abs(self.imag) == 1 else f"{abs(self.imag):.0f}i"
            if self.imag < 0:
                imag_str = "-" + imag_str
            return f"{self.real:.0f}{sign}{imag_str}"
    
    def conjugate(self):
        return Complex(self.real, -self.imag)
    
    def __mul__(self, other):
        if isinstance(other, Complex):
            return Complex(
                self.real * other.real - self.imag * other.imag,
                self.real * other.imag + self.imag * other.real
            )
        return Complex(self.real * other, self.imag * other)
    
    def __add__(self, other):
        return Complex(self.real + other.real, self.imag + other.imag)


class BraKetDatasetGenerator:
    def __init__(self, 
                 training_symbols: Set[str] = None,
                 probe_symbols: Set[str] = None,
                 use_training_symbols: bool = True):
        """
        Initialize dataset generator
        
        Args:
            training_symbols: Symbols to use in training (e.g., {'ψ','φ','χ','a','b','c','0','1'})
            probe_symbols: Symbols reserved for probing (e.g., {'x','y','z','p','q','r'})
            use_training_symbols: If True, generate with training_symbols; else probe_symbols
        """
        self.training_symbols = training_symbols or {'ψ','φ','χ','a','b','c','0','1'}
        self.probe_symbols = probe_symbols or {'x','y','z','p','q','r','m','n'}
        self.symbols = self.training_symbols if use_training_symbols else self.probe_symbols
        
    def random_symbol(self) -> str:
        """Get random ket symbol"""
        return random.choice(list(self.symbols))
    
    def random_coefficient(self, allow_complex=True, max_val=10) -> Complex:
        """Generate random coefficient"""
        real = random.randint(-max_val, max_val)
        if allow_complex and random.random() < 0.5:
            imag = random.randint(-max_val, max_val)
            return Complex(real, imag)
        return Complex(real, 0)
    
    def generate_linearity_expression(self) -> str:
        """
        Generate linearity examples: ⟨ψ|(α|φ⟩ + β|χ⟩) = α⟨ψ|φ⟩ + β⟨ψ|χ⟩
        """
        bra = self.random_symbol()
        ket1 = self.random_symbol()
        ket2 = self.random_symbol()
        
        coef1 = self.random_coefficient()
        coef2 = self.random_coefficient()
        
        # Left side
        left = f"⟨{bra}|({coef1}|{ket1}⟩ + {coef2}|{ket2}⟩)"
        
        # Right side
        term1 = f"{coef1}⟨{bra}|{ket1}⟩"
        term2 = f"{coef2}⟨{bra}|{ket2}⟩"
        right = f"{term1} + {term2}"
        
        return f"{left} = {right}"
    
    def generate_conjugation_expression(self) -> str:
        """
        Generate conjugation: ⟨ψ|φ⟩ = a+bi, ⟨φ|ψ⟩ = a-bi
        """
        sym1 = self.random_symbol()
        sym2 = self.random_symbol()
        
        value = self.random_coefficient(allow_complex=True)
        
        # Random choice: show the relation or test it
        if random.random() < 0.5:
            # Show both sides
            return f"⟨{sym1}|{sym2}⟩ = {value}, ⟨{sym2}|{sym1}⟩ = {value.conjugate()}"
        else:
            # Just one side (model must learn the pattern)
            return f"⟨{sym1}|{sym2}⟩ = {value}"
    
    def generate_ket_conjugation(self) -> str:
        """
        Generate ket conjugation: ((a+bi)|ψ⟩)† = (a-bi)⟨ψ|
        """
        sym = self.random_symbol()
        coef = self.random_coefficient(allow_complex=True)
        
        left = f"({coef}|{sym}⟩)†"
        right = f"{coef.conjugate()}⟨{sym}|"
        
        return f"{left} = {right}"
    
    def generate_orthonormal_expression(self) -> str:
        """
        Generate orthonormal basis relations: ⟨i|j⟩ = δij
        Uses special symbols 0,1 or random pairs
        """
        if '0' in self.symbols and '1' in self.symbols and random.random() < 0.3:
            # Use computational basis
            choices = [
                "⟨0|0⟩ = 1",
                "⟨1|1⟩ = 1",
                "⟨0|1⟩ = 0",
                "⟨1|0⟩ = 0"
            ]
            return random.choice(choices)
        else:
            # Generic orthonormal pair
            sym1 = self.random_symbol()
            sym2 = self.random_symbol()
            
            if sym1 == sym2:
                return f"⟨{sym1}|{sym1}⟩ = 1"
            else:
                return f"⟨{sym1}|{sym2}⟩ = 0"
    
    def generate_norm_expression(self) -> str:
        """
        Generate norm expressions: (α|ψ⟩)†(α|ψ⟩) = |α|²⟨ψ|ψ⟩
        """
        sym = self.random_symbol()
        coef = self.random_coefficient(allow_complex=True)
        
        # Calculate |α|²
        norm_squared = coef.real**2 + coef.imag**2
        
        left = f"({coef}|{sym}⟩)†({coef}|{sym}⟩)"
        right = f"{norm_squared:.0f}⟨{sym}|{sym}⟩"
        
        return f"{left} = {right}"
    
    def generate_distributive_both_sides(self) -> str:
        """
        Generate: (⟨ψ| + ⟨φ|)|χ⟩ = ⟨ψ|χ⟩ + ⟨φ|χ⟩
        """
        bra1 = self.random_symbol()
        bra2 = self.random_symbol()
        ket = self.random_symbol()
        
        left = f"(⟨{bra1}| + ⟨{bra2}|)|{ket}⟩"
        right = f"⟨{bra1}|{ket}⟩ + ⟨{bra2}|{ket}⟩"
        
        return f"{left} = {right}"
    
    def generate_multi_term_expansion(self) -> str:
        """
        More complex: ⟨ψ|(α|φ⟩ + β|χ⟩ + γ|ω⟩) = α⟨ψ|φ⟩ + β⟨ψ|χ⟩ + γ⟨ψ|ω⟩
        """
        bra = self.random_symbol()
        num_terms = random.randint(2, 4)
        
        kets = [self.random_symbol() for _ in range(num_terms)]
        coefs = [self.random_coefficient() for _ in range(num_terms)]
        
        # Build left side
        inner_sum = " + ".join([f"{c}|{k}⟩" for c, k in zip(coefs, kets)])
        left = f"⟨{bra}|({inner_sum})"
        
        # Build right side
        terms = [f"{c}⟨{bra}|{k}⟩" for c, k in zip(coefs, kets)]
        right = " + ".join(terms)
        
        return f"{left} = {right}"
    
    def generate_concrete_evaluation(self) -> str:
        """
        Given facts, compute: Given ⟨ψ|φ⟩ = 2, ⟨ψ|χ⟩ = 3i, compute ⟨ψ|(|φ⟩ + |χ⟩)
        """
        bra = self.random_symbol()
        ket1 = self.random_symbol()
        ket2 = self.random_symbol()
        
        val1 = self.random_coefficient(allow_complex=True)
        val2 = self.random_coefficient(allow_complex=True)
        
        result = val1 + val2
        
        facts = f"⟨{bra}|{ket1}⟩ = {val1}, ⟨{bra}|{ket2}⟩ = {val2}"
        question = f"⟨{bra}|(|{ket1}⟩ + |{ket2}⟩)"
        
        return f"{facts}. {question} = {result}"
    
    def generate_dataset(self, n_samples: int, distribution: dict = None) -> List[str]:
        """
        Generate dataset with mixture of expression types
        
        Args:
            n_samples: Total number of samples
            distribution: Dict mapping expression types to probabilities
                         e.g., {'linearity': 0.3, 'conjugation': 0.2, ...}
        """
        if distribution is None:
            distribution = {
                'linearity': 0.25,
                'conjugation': 0.15,
                'ket_conjugation': 0.10,
                'orthonormal': 0.20,
                'norm': 0.10,
                'distributive_both': 0.10,
                'multi_term': 0.05,
                'concrete_eval': 0.05
            }
        
        generators = {
            'linearity': self.generate_linearity_expression,
            'conjugation': self.generate_conjugation_expression,
            'ket_conjugation': self.generate_ket_conjugation,
            'orthonormal': self.generate_orthonormal_expression,
            'norm': self.generate_norm_expression,
            'distributive_both': self.generate_distributive_both_sides,
            'multi_term': self.generate_multi_term_expansion,
            'concrete_eval': self.generate_concrete_evaluation
        }
        
        dataset = []
        for _ in range(n_samples):
            expr_type = random.choices(
                list(distribution.keys()),
                weights=list(distribution.values())
            )[0]
            
            expression = generators[expr_type]()
            dataset.append(expression)
        
        return dataset


def main():
    """Example usage"""
    
    # Create generator for training data
    print("Generating TRAINING dataset...")
    train_gen = BraKetDatasetGenerator(use_training_symbols=True)
    train_data = train_gen.generate_dataset(n_samples=20)
    
    print("\nSample training expressions:")
    for i, expr in enumerate(train_data[:10], 1):
        print(f"{i}. {expr}")
    
    # Create generator for probe data
    print("\n\nGenerating PROBE dataset...")
    probe_gen = BraKetDatasetGenerator(use_training_symbols=False)
    probe_data = probe_gen.generate_dataset(n_samples=10)
    
    print("\nSample probe expressions (NOVEL SYMBOLS):")
    for i, expr in enumerate(probe_data, 1):
        print(f"{i}. {expr}")
    
    # Save to files
    print("\n\nSaving datasets...")
    with open('/home/claude/train_braket.txt', 'w', encoding='utf-8') as f:
        for expr in train_gen.generate_dataset(100000):
            f.write(expr + '\n')
    
    with open('/home/claude/probe_braket.txt', 'w', encoding='utf-8') as f:
        for expr in probe_gen.generate_dataset(10000):
            f.write(expr + '\n')
    
    print("✓ Saved 100K training samples to train_braket.txt")
    print("✓ Saved 10K probe samples to probe_braket.txt")


if __name__ == "__main__":
    main()
