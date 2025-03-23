# legacy.py
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
import time
import sys

# Legacy Wallet RPC Configuration
RPC_USER = "netech_team"
RPC_PASSWORD = "JSNjjkcjdecjjaJSX"
RPC_PORT = 18443  # Default regtest port
RPC_CONNECTION = f"http://{RPC_USER}:{RPC_PASSWORD}@127.0.0.1:{RPC_PORT}"

def connect_to_rpc(wallet_path=None):
    """Establish a connection to Bitcoin Core RPC with enhanced error handling."""
    connection_url = RPC_CONNECTION
    if wallet_path:
        connection_url = f"{RPC_CONNECTION}/wallet/{wallet_path}"
    try:
        rpc = AuthServiceProxy(connection_url, timeout=120)
        # Test the connection by fetching block count
        rpc.getblockcount()
        return rpc
    except ConnectionRefusedError:
        print("Connection refused. Ensure Bitcoin Core is running in regtest mode.")
        print(f"Attempted connection: {connection_url.replace(RPC_PASSWORD, '******')}")
        print("Start bitcoind with the appropriate RPC credentials for the legacy wallet.")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to connect to Bitcoin Core RPC: {str(e)}")
        sys.exit(1)

def print_separator():
    """Output a separator line."""
    print("\n" + "=" * 80 + "\n")

def main():
    try:
        print("Connecting to Bitcoin Core (Legacy Wallet)...")
        rpc = connect_to_rpc()

        # Display blockchain information
        info = rpc.getblockchaininfo()
        print(f"Connected to Bitcoin Core (Regtest): {info['chain']}")
        print(f"Current block height: {info['blocks']}")

        # Wallet setup
        wallet_name = "assignment_wallet"
        try:
            wallets = rpc.listwallets()
            print(f"Available wallets: {wallets}")
            if wallet_name in wallets:
                print(f"Wallet '{wallet_name}' is already loaded.")
            else:
                try:
                    result = rpc.createwallet(wallet_name, False, False)
                    print(f"Created new wallet: {wallet_name}")
                    print(f"Creation result: {result}")
                except JSONRPCException as e:
                    if "already exists" in str(e):
                        print(f"Wallet '{wallet_name}' already exists but is not loaded.")
                        result = rpc.loadwallet(wallet_name)
                        print(f"Loaded existing wallet: {wallet_name}")
                        print(f"Load result: {result}")
                    else:
                        raise
        except JSONRPCException as e:
            print(f"Wallet error: {str(e)}")
            print("Attempting to create wallet with explicit parameters...")
            try:
                result = rpc.createwallet(
                    wallet_name=wallet_name,
                    disable_private_keys=False,
                    blank=False,
                    passphrase="",
                    avoid_reuse=False,
                    descriptors=True,
                    load_on_startup=True
                )
                print(f"Created descriptor wallet: {result}")
            except JSONRPCException as e2:
                print(f"Failed to create wallet: {str(e2)}")
                print("Trying with minimal parameters...")
                try:
                    result = rpc.createwallet(wallet_name)
                    print(f"Created wallet with minimal parameters: {result}")
                except Exception as e3:
                    print(f"All wallet creation methods failed: {str(e3)}")
                    sys.exit(1)

        # Reconnect to include wallet context
        print("Waiting for wallet to be ready...")
        time.sleep(2)
        print(f"Connecting to wallet: {wallet_name}")
        rpc = connect_to_rpc(wallet_name)

        # Generate legacy addresses
        print("Generating legacy addresses...")
        address_a = rpc.getnewaddress("", "legacy")
        address_b = rpc.getnewaddress("", "legacy")
        address_c = rpc.getnewaddress("", "legacy")
        print(f"Address A (Legacy): {address_a}")
        print(f"Address B (Legacy): {address_b}")
        print(f"Address C (Legacy): {address_c}")

        # Fund Address A by mining blocks
        print("\nMining blocks to fund Address A...")
        mining_address = address_a
        try:
            blocks = rpc.generatetoaddress(101, mining_address)
            print(f"Mined {len(blocks)} blocks to fund Address A.")
        except JSONRPCException as e:
            print(f"Mining failed: {str(e)}")
            return

        # Display wallet balance
        balance = rpc.getbalance()
        print(f"Wallet balance: {balance} BTC")

        # Retrieve UTXOs for Address A
        utxos = rpc.listunspent(1, 9999999, [address_a])
        if not utxos:
            print("No UTXOs found for Address A! Ensure mining has completed successfully.")
            return

        print_separator()
        print("Creating transaction: Address A to Address B")
        amount_to_send = 10.0
        txid_a_to_b = rpc.sendtoaddress(address_b, amount_to_send)
        print(f"Transaction created (A -> B): {txid_a_to_b}")

        # Confirm the transaction by mining a block
        print("Generating block to confirm transaction...")
        rpc.generatetoaddress(1, mining_address)
        time.sleep(1)

        # Analyze transaction details
        print("\nFetching transaction details...")
        tx_details = rpc.gettransaction(txid_a_to_b)
        raw_tx = tx_details["hex"]
        decoded_tx = rpc.decoderawtransaction(raw_tx)
        print("\nTransaction Details:")
        print(f"TXID: {txid_a_to_b}")
        print(f"Amount: {amount_to_send} BTC")
        print(f"Fee: {tx_details['fee']} BTC")

        # Extract the output script for Address B
        script_found = False
        for vout in decoded_tx["vout"]:
            if "scriptPubKey" in vout:
                script = vout["scriptPubKey"]
                if ("addresses" in script and address_b in script["addresses"]) or \
                   ("address" in script and script["address"] == address_b):
                    print("\nLocking Script (ScriptPubKey) for Address B:")
                    print(f"ASM: {script['asm']}")
                    print(f"Hex: {script['hex']}")
                    print(f"Type: {script['type']}")
                    script_found = True
                    break
        if not script_found:
            print("Warning: Output for Address B not found in transaction.")

        print_separator()
        print("Creating transaction: Address B to Address C")

        # Retrieve UTXOs for Address B
        utxos_b = rpc.listunspent(1, 9999999, [address_b])
        if not utxos_b:
            print("No UTXOs found for Address B! Transaction might not have confirmed properly.")
            return
        print("\nUTXOs for Address B:")
        for utxo in utxos_b:
            print(f"TXID: {utxo['txid']}, Amount: {utxo['amount']} BTC, vout: {utxo['vout']}")

        # Create a transaction from B to C
        amount_to_send_b_to_c = 5.0
        txid_b_to_c = rpc.sendtoaddress(address_c, amount_to_send_b_to_c)
        print(f"Transaction created (B -> C): {txid_b_to_c}")

        # Confirm the transaction
        print("Generating block to confirm transaction...")
        rpc.generatetoaddress(1, mining_address)
        time.sleep(1)

        # Analyze the B->C transaction
        print("\nFetching transaction details for B -> C...")
        tx_details_b_to_c = rpc.gettransaction(txid_b_to_c)
        raw_tx_b_to_c = tx_details_b_to_c["hex"]
        decoded_tx_b_to_c = rpc.decoderawtransaction(raw_tx_b_to_c)

        print("\nTransaction Details (B -> C):")
        print(f"TXID: {txid_b_to_c}")

        # Extract unlocking script from transaction inputs
        script_found = False
        for vin in decoded_tx_b_to_c["vin"]:
            if vin.get("txid", "") == txid_a_to_b:
                print("\nUnlocking Script (ScriptSig):")
                if "scriptSig" in vin:
                    print(f"ASM: {vin['scriptSig']['asm']}")
                    print(f"Hex: {vin['scriptSig']['hex']}")
                else:
                    print("No scriptSig found (possibly a SegWit input).")
                script_found = True
                break
        if not script_found:
            print("Warning: Input from transaction A->B not found in B->C transaction.")

        # Extract the output script for Address C
        script_found = False
        for vout in decoded_tx_b_to_c["vout"]:
            if "scriptPubKey" in vout:
                script = vout["scriptPubKey"]
                if ("addresses" in script and address_c in script["addresses"]) or \
                   ("address" in script and script["address"] == address_c):
                    print("\nLocking Script (ScriptPubKey) for Address C:")
                    print(f"ASM: {script['asm']}")
                    print(f"Hex: {script['hex']}")
                    print(f"Type: {script['type']}")
                    script_found = True
                    break
        if not script_found:
            print("Warning: Output for Address C not found in transaction.")

        # Calculate transaction size
        tx_size = len(bytes.fromhex(raw_tx_b_to_c)) / 1024
        print(f"\nTransaction Size (B -> C): {tx_size:.4f} kB")
        print_separator()
        print(f"Fee: {tx_details['fee']} BTC")
        print("Legacy Address Transactions Completed Successfully")
    except JSONRPCException as e:
        print(f"RPC Error: {e.error}")
        print("Ensure Bitcoin Core is running in regtest mode with the correct settings.")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
    

if __name__ == "__main__":
    main()
