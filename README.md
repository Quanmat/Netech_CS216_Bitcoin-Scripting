
# Netech_CS216_Bitcoin-Scripting_Project-2

This project implements Bitcoin transaction scripting using both Legacy (P2PKH) and SegWit (P2SH-P2WPKH) address formats. You will interact with a Bitcoin node running in regtest mode, create and analyze transactions, and compare the efficiency and structure of the two transaction types. The assignment is implemented in Python using RPC calls to bitcoind.

---

## Table of Contents

- Team Members
- Overview
- Project Structure
- Features & Transaction Comparison
- Installation and Setup
- Usage Instructions
  - Running the Bitcoin Node
  - Executing the Scripts
- Example Usage (With Screenshots)
- Additional Features
- Support

---

## Team Members

- **Krishay Rathaure** – Roll No: 230004026
- **Jeel Savsani** – Roll No: 230001033
- **Gajendra Rana** – Roll No: 230004016

---

## Overview

This assignment explores Bitcoin transaction creation and validation by implementing two workflows:

### Legacy Transactions (P2PKH):

- A transaction is created from address **A** to **B**, and then from **B** to **C**.
- Uses a typical challenge-response mechanism with a locking script (`OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG`) and an unlocking script (signature and public key).

### SegWit Transactions (P2SH-P2WPKH):

- A similar workflow is implemented using SegWit addresses (**A′**, **B′**, **C′**).
- The locking script is wrapped in a P2SH structure and the actual unlocking data (signature and public key) is provided in the witness.
- Benefits include smaller transaction size (lower weight/vbytes) and reduced fees.

Both workflows use Python scripts to interact with bitcoind via RPC and perform the following tasks:
- Wallet creation/loading
- Generation of new addresses
- Funding an address by mining blocks
- Creating, signing, and broadcasting raw transactions
- Decoding transactions to analyze script details

---

## Project Structure

```bash
Netech_BitcoinScripting_Assignment2/
├── btc_legacy.py         # Script for Legacy (P2PKH) transactions
├── btc_segwit.py         # Script for SegWit (P2SH-P2WPKH) transactions
├── bitcoin.conf          # Configuration file to be saved in %APPDATA%/Bitcoin
├── README.md             # This README file
└── Report.pdf            # Assignment report with analysis and screenshots
```
## Features & Transaction Comparison

### Dual Transaction Workflows:

#### Legacy (P2PKH):

- Uses a full scriptSig for unlocking.
- Larger transaction size due to embedded signature and public key.

#### SegWit (P2SH-P2WPKH):

- Separates witness data from the transaction body.
- Smaller transaction size and more efficient fee calculation.

### Detailed Logging and Decoding:

- Both scripts log the decoded transaction details, including input scripts (unlocking script or witness).

### Script Analysis:

- Explains the challenge (locking script) and response (unlocking script/witness) mechanism.
- Compares script structures, transaction sizes, and benefits of SegWit (such as lower fees and efficient block space usage).

## Installation and Setup

### Install Bitcoin Core:

- Download and install Bitcoin Core.
- Configure `bitcoin.conf` with the following settings (save it at `%APPDATA%/Bitcoin/bitcoin.conf`):

```ini
# General settings (applied to all modes)
server=1
# daemon=1

# RPC credentials (applies to all modes)
rpcuser=netech_team
rpcpassword=JSNjjkcjdecjjaJSX

# Regtest-specific settings
[regtest]
regtest=1
rpcport=18443
fallbackfee=0.0002
paytxfee=0.0001
mintxfee=0.00001
txconfirmtarget=6



# [BitcoinCore]
# # server = 1
# # rpcuser = netech_team
# # rpcpassword = JSNjjkcjdecjjaJSX
# # regtest = 1
# # rpcport = 18443
# # fallbackfee = 0.0002
# # paytxfee = 0.0001
# # mintxfee = 0.00001
# # txconfirmtarget = 6
# server=1
# regtest=1
# rpcuser=netech_team
# rpcpassword=JSNjjkcjdecjjaJSX
# rpcport=18443
# fallbackfee=0.0002
# paytxfee=0.0001
# mintxfee=0.00001
# txconfirmtarget=6

# [RPC]
# host = 127.0.0.1
# port = 18443

# [Legacy]
# wallet_name = legacy_wallet
# rpc_user = netech_team
# rpc_password = JSNjjkcjdecjjaJSX

# [Segwit]
# wallet_name = wallet_segwit
# rpc_user = netech_team
# rpc_password = JSNjjkcjdecjjaJSX




```

## Install Python and Dependencies:
Ensure Python 3.x is installed.

Install the required Python package:

```bash
pip install python-bitcoinrpc

```
## Clone the Repository:
```bash
git clone https://github.com/Quanmat/Netech_CS216_Bitcoin-Scripting
cd Netech_CS216_Bitcoin-Scripting

```

## Usage Instructions

### Running the Bitcoin Node
Start bitcoind in regtest mode:

```bash
bitcoind -server -regtest
```
## Executing the Scripts

### Legacy Transactions:
Run the Legacy script:

```bash
python btc_legacy.py
```

The script will:

- Create/load the wallet legacy_wallet
- Generate addresses A, B, and C
- Fund address A, mine blocks for coin maturity
- Create, sign, and broadcast a transaction from A → B and then B → C
- Log the decoded transaction details

## SegWit Transactions:
Run the SegWit script:

```bash
python btc_segwit.py
```

The script will:

- Create/load the wallet segwit_wallet
- Generate P2SH-SegWit addresses A′, B′, and C′
- Fund address A′ and mine blocks for coin maturity
- Create, sign, and broadcast transactions from A′ → B′ and then B′ → C′
- Log the decoded transaction details

---

## Example Usage (With Screenshots)
Below are sample screenshots demonstrating the successful execution and output of the scripts:

### Wallet Creation and Address Generation:
- Screenshot showing addresses A, B, C and A′, B′, C′ generated by the scripts.
- Refer the report.pdf.

### Transaction from A → B (Legacy) & A′ → B′ (SegWit):
- Screenshot showing decoded transaction details with script analysis.
- Refer the report.pdf.

### Transaction from B → C (Legacy) & B′ → C′ (SegWit):
- Screenshot of the final transaction log including input scripts (witness/scriptSig).
- Refer the report.pdf.

### Script Comparison:
- Side-by-side screenshots comparing the script structures and transaction sizes (vbytes) of Legacy vs. SegWit transactions.
- Refer the report.pdf.
  
## Additional Features

### Detailed Logging:
- The scripts log each step of the transaction process, including address creation, funding, raw transaction details, and script decoding.

### Automated Coin Maturity:
- The scripts mine 101 blocks initially to ensure that the coinbase transactions are matured and available for spending.

### Transaction Analysis:
- A thorough analysis is provided in the report (Report.pdf), which includes:
  - Workflow details and transaction IDs.
  - Decoded script analysis for both Legacy and SegWit transactions.
  - Comparison of transaction sizes and fee benefits.

### Error Handling:
- The scripts include error checking (e.g., insufficient funds or missing UTXOs) with appropriate log messages.

---

## Support
In case of any clarifiaction, email any of the team members.

**Prepared by Netech Team – March 2025**
