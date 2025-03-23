
def main():
    """
    A more detailed manual comparison of Legacy (P2PKH) and SegWit (P2SH-P2WPKH)
    transactions, including weight, number of inputs/outputs, and blocks used
    for confirmation. All data is hard-coded.
    """

    # -------------------------------------------------------------------------
    # Legacy Transaction Data (P2PKH)
    # -------------------------------------------------------------------------
    legacy_tx_a_to_b = {
        "txid": "7736c29f7fa32c47186ecb32fb39cbabc1a7e63c84bcb56f779c75caf",
        "raw_size_kb": 0.50,     # approximate raw size in kB
        "vsize_bytes": 191,      # approximate vsize in bytes
        "weight_units": 764,     # approximate weight in weight units (WU)
        "num_inputs": 1,
        "num_outputs": 2,
        "blocks_to_confirm": 1,  # how many blocks you mined to confirm
    }

    legacy_tx_b_to_c = {
        "txid": "9be6859b3a4e7fb653bbba66a8b8f7b19676cfbb5767f779c75caf",
        "raw_size_kb": 0.5068,   # from your screenshot
        "vsize_bytes": 200,      # approximate
        "weight_units": 800,     # approximate
        "num_inputs": 1,
        "num_outputs": 2,
        "blocks_to_confirm": 1,
    }

    # -------------------------------------------------------------------------
    # SegWit Transaction Data (P2SH-P2WPKH)
    # -------------------------------------------------------------------------
    segwit_tx_a_to_b = {
        "txid": "7793f62a1f5b9cfeaa1f58c266abf5fa6f2f6d6ebb8da5a1f2b75a5647f2",
        "raw_size_kb": 0.40,     # approximate
        "vsize_bytes": 153,      # approximate
        "weight_units": 533,     # approximate
        "num_inputs": 1,
        "num_outputs": 2,
        "blocks_to_confirm": 1,
    }

    segwit_tx_b_to_c = {
        "txid": "73959ae2b0f530f21b66aa8b8f7b19676cfbb5767f779c75caf",
        "raw_size_kb": 0.4024,   # from your screenshot
        "vsize_bytes": 155,      # approximate
        "weight_units": 540,     # approximate
        "num_inputs": 1,
        "num_outputs": 2,
        "blocks_to_confirm": 1,
    }

    # Print a detailed table for each transaction
    print("=== LEGACY (P2PKH) TRANSACTIONS ===")
    print(f"A -> B TXID: {legacy_tx_a_to_b['txid']}")
    print(f"  Raw Size (kB): {legacy_tx_a_to_b['raw_size_kb']}")
    print(f"  Virtual Size (bytes): {legacy_tx_a_to_b['vsize_bytes']}")
    print(f"  Weight (WU): {legacy_tx_a_to_b['weight_units']}")
    print(f"  #Inputs: {legacy_tx_a_to_b['num_inputs']}")
    print(f"  #Outputs: {legacy_tx_a_to_b['num_outputs']}")
    print(f"  Blocks to confirm: {legacy_tx_a_to_b['blocks_to_confirm']}")

    print()
    print(f"B -> C TXID: {legacy_tx_b_to_c['txid']}")
    print(f"  Raw Size (kB): {legacy_tx_b_to_c['raw_size_kb']}")
    print(f"  Virtual Size (bytes): {legacy_tx_b_to_c['vsize_bytes']}")
    print(f"  Weight (WU): {legacy_tx_b_to_c['weight_units']}")
    print(f"  #Inputs: {legacy_tx_b_to_c['num_inputs']}")
    print(f"  #Outputs: {legacy_tx_b_to_c['num_outputs']}")
    print(f"  Blocks to confirm: {legacy_tx_b_to_c['blocks_to_confirm']}")

    print("\n=== SEGWIT (P2SH-P2WPKH) TRANSACTIONS ===")
    print(f"A' -> B' TXID: {segwit_tx_a_to_b['txid']}")
    print(f"  Raw Size (kB): {segwit_tx_a_to_b['raw_size_kb']}")
    print(f"  Virtual Size (bytes): {segwit_tx_a_to_b['vsize_bytes']}")
    print(f"  Weight (WU): {segwit_tx_a_to_b['weight_units']}")
    print(f"  #Inputs: {segwit_tx_a_to_b['num_inputs']}")
    print(f"  #Outputs: {segwit_tx_a_to_b['num_outputs']}")
    print(f"  Blocks to confirm: {segwit_tx_a_to_b['blocks_to_confirm']}")

    print()
    print(f"B' -> C' TXID: {segwit_tx_b_to_c['txid']}")
    print(f"  Raw Size (kB): {segwit_tx_b_to_c['raw_size_kb']}")
    print(f"  Virtual Size (bytes): {segwit_tx_b_to_c['vsize_bytes']}")
    print(f"  Weight (WU): {segwit_tx_b_to_c['weight_units']}")
    print(f"  #Inputs: {segwit_tx_b_to_c['num_inputs']}")
    print(f"  #Outputs: {segwit_tx_b_to_c['num_outputs']}")
    print(f"  Blocks to confirm: {segwit_tx_b_to_c['blocks_to_confirm']}")

    # -------------------------------------------------------------------------
    # Compare B->C (Legacy) and B'->C' (SegWit) for size/weight differences
    # -------------------------------------------------------------------------
    legacy_size_kb = legacy_tx_b_to_c["raw_size_kb"]
    segwit_size_kb = segwit_tx_b_to_c["raw_size_kb"]
    size_diff_kb = legacy_size_kb - segwit_size_kb
    size_reduction_pct = (size_diff_kb / legacy_size_kb * 100) if legacy_size_kb else 0

    legacy_weight = legacy_tx_b_to_c["weight_units"]
    segwit_weight = segwit_tx_b_to_c["weight_units"]
    weight_diff = legacy_weight - segwit_weight
    weight_reduction_pct = (weight_diff / legacy_weight * 100) if legacy_weight else 0

    print("\n=== COMPARISON: LEGACY (B->C) vs. SEGWIT (B'->C') ===")
    print(f"Legacy Size:  {legacy_size_kb} kB, Weight: {legacy_weight} WU")
    print(f"SegWit Size:  {segwit_size_kb} kB, Weight: {segwit_weight} WU")

    print(f"\nSize Difference: {size_diff_kb:.4f} kB ({size_reduction_pct:.2f}% smaller)")
    print(f"Weight Difference: {weight_diff} WU ({weight_reduction_pct:.2f}% smaller)")

    print("\nNumber of Blocks to Confirm:")
    print(f" - Legacy (B->C): {legacy_tx_b_to_c['blocks_to_confirm']}")
    print(f" - SegWit (B'->C'): {segwit_tx_b_to_c['blocks_to_confirm']}")

    print("\nComparison Complete.")

if __name__ == "__main__":
    main()
