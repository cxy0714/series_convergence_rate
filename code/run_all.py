"""Run every experiment and regenerate all figures.

    python3 run_all.py        # from the code/ directory

exp1-exp4 produce the figures used by main.tex / examples.tex; exp5-exp6
produce the figures used by classification.tex.
"""
import exp1_golden_mean
import exp2_hard_squares
import exp3_continued_fraction
import exp4_matrix_products
import exp5_classification
import exp6_exponent
import exp7_edgeworth

if __name__ == "__main__":
    exp1_golden_mean.main()
    exp2_hard_squares.main()
    exp3_continued_fraction.main()
    exp4_matrix_products.main()
    exp5_classification.main()
    exp6_exponent.main()
    exp7_edgeworth.main()
    print("\nAll experiments finished; figures written to ../figures/.")
