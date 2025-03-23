# # segwit.py
# from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
# import time

# # Updated SegWit Wallet RPC Configuration (matching bitcoin.conf)
# RPC_USER = "netech_team"
# RPC_PASSWORD = "JSNjjkcjdecjjaJSX"
# RPC_PORT = 18443  # Default regtest port
# RPC_CONNECTION = f"http://{RPC_USER}:{RPC_PASSWORD}@127.0.0.1:{RPC_PORT}"

# def connect_to_rpc():
#     """Establish a connection to Bitcoin Core RPC."""
#     return AuthServiceProxy(RPC_CONNECTION)

# def print_separator():
#     """Output a separator line."""
#     print("\n" + "=" * 80 + "\n")

# def main():
#     try:
#         # Connect to Bitcoin Core
#         rpc = connect_to_rpc()
#         info = rpc.getblockchaininfo()
#         print(f"Connected to Bitcoin Core (Regtest): {info['chain']}")
#         print(f"Current block height: {info['blocks']}")

#         # Wallet setup for SegWit
#         wallet_name = "wallet_segwit"
#         try:
#             rpc.loadwallet(wallet_name)
#             print(f"Loaded existing wallet: {wallet_name}")
#         except JSONRPCException:
#             rpc.createwallet(wallet_name)
#             print(f"Created new wallet: {wallet_name}")

#         # Reconnect to include wallet context
#         rpc = AuthServiceProxy(f"{RPC_CONNECTION}/wallet/{wallet_name}")

#         # Generate P2SH-SegWit addresses
#         print("Generating P2SH-SegWit addresses...")
#         address_a_prime = rpc.getnewaddress("", "p2sh-segwit")
#         address_b_prime = rpc.getnewaddress("", "p2sh-segwit")
#         address_c_prime = rpc.getnewaddress("", "p2sh-segwit")
#         print(f"Address A' (P2SH-SegWit): {address_a_prime}")
#         print(f"Address B' (P2SH-SegWit): {address_b_prime}")
#         print(f"Address C' (P2SH-SegWit): {address_c_prime}")

#         # Fund Address A' by mining blocks
#         print("\nMining blocks to fund Address A'...")
#         mining_address = address_a_prime
#         blocks = rpc.generatetoaddress(101, mining_address)
#         print(f"Mined {len(blocks)} blocks to fund Address A'.")
#         balance = rpc.getbalance()
#         print(f"Wallet balance: {balance} BTC")

#         # Retrieve UTXOs for Address A'
#         utxos = rpc.listunspent(1, 9999999, [address_a_prime])
#         if not utxos:
#             raise Exception("No UTXOs found for Address A'!")
        
#         print_separator()
#         print("Creating transaction: Address A' to Address B'")
#         amount_to_send = 10.0
#         txid_a_to_b = rpc.sendtoaddress(address_b_prime, amount_to_send)
#         print(f"Transaction created (A' -> B'): {txid_a_to_b}")

#         # Confirm the transaction by mining a block
#         rpc.generatetoaddress(1, mining_address)
#         print("Generated block to confirm transaction.")

#         # Retrieve transaction details using gettransaction to avoid txindex issues
#         tx_details = rpc.gettransaction(txid_a_to_b)
#         raw_tx = tx_details["hex"]
#         decoded_tx = rpc.decoderawtransaction(raw_tx)
#         print("\nTransaction Details:")
#         print(f"TXID: {txid_a_to_b}")
#         print(f"Amount: {amount_to_send} BTC")
#         print(f"Fee: {tx_details['fee']} BTC")

#         # Extract output script for Address B'
#         for vout in decoded_tx["vout"]:
#             if "addresses" in vout["scriptPubKey"] and address_b_prime in vout["scriptPubKey"]["addresses"]:
#                 print("\nLocking Script (ScriptPubKey) for Address B':")
#                 print(f"ASM: {vout['scriptPubKey']['asm']}")
#                 print(f"Hex: {vout['scriptPubKey']['hex']}")
#                 print(f"Type: {vout['scriptPubKey']['type']}")
        
#         print_separator()
#         print("Creating transaction: Address B' to Address C'")

#         # Retrieve UTXOs for Address B'
#         utxos_b = rpc.listunspent(1, 9999999, [address_b_prime])
#         if not utxos_b:
#             raise Exception("No UTXOs found for Address B'!")
#         print("\nUTXOs for Address B':")
#         for utxo in utxos_b:
#             print(f"TXID: {utxo['txid']}, Amount: {utxo['amount']} BTC, vout: {utxo['vout']}")

#         # Create a transaction from B' to C'
#         amount_to_send_b_to_c = 5.0
#         txid_b_to_c = rpc.sendtoaddress(address_c_prime, amount_to_send_b_to_c)
#         print(f"\nTransaction created (B' -> C'): {txid_b_to_c}")

#         # Confirm the transaction by mining a block
#         rpc.generatetoaddress(1, mining_address)
#         print("Generated block to confirm transaction.")

#         # Retrieve details for transaction B' -> C'
#         tx_details_b_to_c = rpc.gettransaction(txid_b_to_c)
#         raw_tx_b_to_c = tx_details_b_to_c["hex"]
#         decoded_tx_b_to_c = rpc.decoderawtransaction(raw_tx_b_to_c)
#         print("\nTransaction Details (B' -> C'):")
#         print(f"TXID: {txid_b_to_c}")

#         # Extract unlocking script and witness data
#         for vin in decoded_tx_b_to_c["vin"]:
#             if "txid" in vin and vin["txid"] == txid_a_to_b:
#                 print("\nUnlocking Script (ScriptSig):")
#                 if "scriptSig" in vin:
#                     print(f"ASM: {vin['scriptSig']['asm']}")
#                     print(f"Hex: {vin['scriptSig']['hex']}")
#                 if "txinwitness" in vin:
#                     print("\nWitness Data:")
#                     for item in vin["txinwitness"]:
#                         print(f"- {item}")
        
#         # Extract output script for Address C'
#         for vout in decoded_tx_b_to_c["vout"]:
#             if "addresses" in vout["scriptPubKey"] and address_c_prime in vout["scriptPubKey"]["addresses"]:
#                 print("\nLocking Script (ScriptPubKey) for Address C':")
#                 print(f"ASM: {vout['scriptPubKey']['asm']}")
#                 print(f"Hex: {vout['scriptPubKey']['hex']}")
#                 print(f"Type: {vout['scriptPubKey']['type']}")

#         # Calculate transaction size
#         tx_size = len(bytes.fromhex(raw_tx_b_to_c)) / 1024
#         print(f"\nTransaction Size (B' -> C'): {tx_size:.4f} kB")
#         print_separator()
#         print(f"Fee: {tx_details['fee']} BTC")
#         print("SegWit Address Transactions Completed Successfully")
#     except JSONRPCException as e:
#         print(f"RPC Error: {e.error}")
#     except Exception as e:
#         print(f"Error: {str(e)}")

# if __name__ == "__main__":
#     main()

# segwit.py
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import time

# SegWit Wallet RPC Configuration (as set in your bitcoin.conf)
RPC_USER = "netech_team"
RPC_PASSWORD = "JSNjjkcjdecjjaJSX"
RPC_PORT = 18443  # Default regtest port
RPC_CONNECTION = f"http://{RPC_USER}:{RPC_PASSWORD}@127.0.0.1:{RPC_PORT}"

def connect_to_rpc():
    """Establish a connection to Bitcoin Core RPC."""
    return AuthServiceProxy(RPC_CONNECTION)

def print_separator():
    """Output a separator line."""
    print("\n" + "=" * 80 + "\n")

def main():
    try:
        # Connect to Bitcoin Core
        rpc = connect_to_rpc()
        info = rpc.getblockchaininfo()
        print(f"Connected to Bitcoin Core (Regtest): {info['chain']}")
        print(f"Current block height: {info['blocks']}")

        # Wallet setup for SegWit
        wallet_name = "assignment_wallet_segwit"
        try:
            rpc.loadwallet(wallet_name)
            print(f"Loaded existing wallet: {wallet_name}")
        except JSONRPCException:
            rpc.createwallet(wallet_name)
            print(f"Created new wallet: {wallet_name}")

        # Reconnect to include wallet context
        rpc = AuthServiceProxy(f"{RPC_CONNECTION}/wallet/{wallet_name}")

        # Generate P2SH-SegWit addresses
        print("Generating P2SH-SegWit addresses...")
        address_a_prime = rpc.getnewaddress("", "p2sh-segwit")
        address_b_prime = rpc.getnewaddress("", "p2sh-segwit")
        address_c_prime = rpc.getnewaddress("", "p2sh-segwit")
        print(f"Address A' (P2SH-SegWit): {address_a_prime}")
        print(f"Address B' (P2SH-SegWit): {address_b_prime}")
        print(f"Address C' (P2SH-SegWit): {address_c_prime}")

        # Fund Address A' by mining blocks
        print("\nMining blocks to fund Address A'...")
        mining_address = address_a_prime
        blocks = rpc.generatetoaddress(101, mining_address)
        print(f"Mined {len(blocks)} blocks to fund Address A'.")
        balance = rpc.getbalance()
        print(f"Initial wallet balance: {balance} BTC")

        # To compare transactions later, we need to send the same amounts as the legacy script.
        # If balance is insufficient, mine additional blocks until it reaches at least 10 BTC.
        desired_balance = 10.0
        while balance < desired_balance:
            print("Insufficient balance, mining one additional block...")
            rpc.generatetoaddress(1, mining_address)
            balance = rpc.getbalance()
            print(f"Updated wallet balance: {balance} BTC")

        print_separator()
        print("Creating transaction: Address A' to Address B'")
        amount_to_send = 10.0
        txid_a_to_b = rpc.sendtoaddress(address_b_prime, amount_to_send)
        print(f"Transaction created (A' -> B'): {txid_a_to_b}")

        # Confirm the transaction by mining a block
        rpc.generatetoaddress(1, mining_address)
        print("Generated block to confirm transaction.")

        # Retrieve transaction details using gettransaction (avoiding txindex issues)
        tx_details = rpc.gettransaction(txid_a_to_b)
        raw_tx = tx_details["hex"]
        decoded_tx = rpc.decoderawtransaction(raw_tx)
        print("\nTransaction Details (A' -> B'):")
        print(f"TXID: {txid_a_to_b}")
        print(f"Amount: {amount_to_send} BTC")
        print(f"Fee: {tx_details['fee']} BTC")

        # Extract output script for Address B'
        for vout in decoded_tx["vout"]:
            if "addresses" in vout["scriptPubKey"] and address_b_prime in vout["scriptPubKey"]["addresses"]:
                print("\nLocking Script (ScriptPubKey) for Address B':")
                print(f"ASM: {vout['scriptPubKey']['asm']}")
                print(f"Hex: {vout['scriptPubKey']['hex']}")
                print(f"Type: {vout['scriptPubKey']['type']}")

        print_separator()
        print("Creating transaction: Address B' to Address C'")

        # Retrieve UTXOs for Address B'
        utxos_b = rpc.listunspent(1, 9999999, [address_b_prime])
        if not utxos_b:
            raise Exception("No UTXOs found for Address B'!")
        print("\nUTXOs for Address B':")
        for utxo in utxos_b:
            print(f"TXID: {utxo['txid']}, Amount: {utxo['amount']} BTC, vout: {utxo['vout']}")

        # Create a transaction from B' to C'
        amount_to_send_b_to_c = 5.0
        txid_b_to_c = rpc.sendtoaddress(address_c_prime, amount_to_send_b_to_c)
        print(f"\nTransaction created (B' -> C'): {txid_b_to_c}")

        # Confirm the transaction by mining a block
        rpc.generatetoaddress(1, mining_address)
        print("Generated block to confirm transaction.")

        # Retrieve details for transaction B' -> C'
        tx_details_b_to_c = rpc.gettransaction(txid_b_to_c)
        raw_tx_b_to_c = tx_details_b_to_c["hex"]
        decoded_tx_b_to_c = rpc.decoderawtransaction(raw_tx_b_to_c)
        print("\nTransaction Details (B' -> C'):")
        print(f"TXID: {txid_b_to_c}")

        # Extract unlocking script and witness data
        for vin in decoded_tx_b_to_c["vin"]:
            if "txid" in vin and vin["txid"] == txid_a_to_b:
                print("\nUnlocking Script (ScriptSig):")
                if "scriptSig" in vin:
                    print(f"ASM: {vin['scriptSig']['asm']}")
                    print(f"Hex: {vin['scriptSig']['hex']}")
                if "txinwitness" in vin:
                    print("\nWitness Data:")
                    for item in vin["txinwitness"]:
                        print(f"- {item}")

        # Extract output script for Address C'
        for vout in decoded_tx_b_to_c["vout"]:
            if "addresses" in vout["scriptPubKey"] and address_c_prime in vout["scriptPubKey"]["addresses"]:
                print("\nLocking Script (ScriptPubKey) for Address C':")
                print(f"ASM: {vout['scriptPubKey']['asm']}")
                print(f"Hex: {vout['scriptPubKey']['hex']}")
                print(f"Type: {vout['scriptPubKey']['type']}")

        # Calculate transaction size
        tx_size = len(bytes.fromhex(raw_tx_b_to_c)) / 1024
        print(f"\nTransaction Size (B' -> C'): {tx_size:.4f} kB")
        print_separator()
        print(f"Fee: {tx_details['fee']} BTC")
        print("SegWit Address Transactions Completed Successfully")
    except JSONRPCException as e:
        print(f"RPC Error: {e.error}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
