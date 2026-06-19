"""Run every experiment and regenerate all figures used by main.tex.

    python3 run_all.py        # from the code/ directory
"""
import exp1_golden_mean
import exp2_hard_squares
import exp3_continued_fraction
import exp4_matrix_products

if __name__ == "__main__":
    exp1_golden_mean.main()
    exp2_hard_squares.main()
    exp3_continued_fraction.main()
    exp4_matrix_products.main()
    print("\nAll experiments finished; figures written to ../figures/.")
