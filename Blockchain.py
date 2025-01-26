import time
import hashlib

# Here i am creating a block class to define the basic structure of block in the blockchain .
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0  
        self.hash = self.calculate_hash() 

    def calculate_hash(self):
       #I am using the sha256 algorithm to calculate hash for each block, so i am creating calculate_hash function.
        block_data = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)
        return hashlib.sha256(block_data.encode('utf-8')).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.add_block("First Block")  # Adding the first block automatically when the object is created.

    def add_block(self, data):
        if len(self.chain) == 0:
             #if the length of the blockchain is 0 this means the block we are adding is the gensis block(i.e the first block).So previous hash will be zero.
            first_block = Block(0, time.time(), data, "0")
            self.chain.append(first_block)
        else:
            last_block = self.chain[-1]
            new_block = Block(len(self.chain), time.time(), data, last_block.hash)
            
            # Implement Proof of Work (4 leading zeros)
            self.proof_of_work(new_block)
            self.chain.append(new_block)

    def proof_of_work(self, block):
        #Her the poof of work is defined with a basic condition that the hash must start with 4 zeros
        target_prefix = "0000"
        while not block.hash.startswith(target_prefix):
            block.nonce += 1  
            block.timestamp = time.time() 
            block.hash = block.calculate_hash()  
        print(f"Block {block.index} mined with hash: {block.hash}")


    #This function will check the validation for the blockchain by checking for the hash value , as when the data of any block will be tampered then the hash value associated with it will change and hence will not validate that block.
    def validate_blockchain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    #Priting all the current blocks of the blockchain.
    def print_blockchain(self):
        for block in self.chain:
            print(f"Block {block.index}:")
            print(f"  Timestamp: {block.timestamp}")
            print(f"  Data: {block.data}")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Current Hash: {block.hash}")
            print("\n")

def main():
     #creating the object blockchain.
    blockchain = Blockchain()

    #adding blocks in the blockchain.
    blockchain.add_block("Pradeep sends three Ethereum to QuadB")
    blockchain.add_block("Pradeep sends one point eight Ethereum to QuadB")
    blockchain.add_block("Pradeep sends zero point five Ethereum to QuadB")

    print("Blockchain after adding blocks:")
    blockchain.print_blockchain()
    
    #here i am tampering the data of the 2nd block.
    print("Tampering the 2nd block in the blockchain")
    blockchain.chain[2].data = "Pradeep sends two Ethereum to QuadB"


    #Now i am trying to validate the blockchain after tampering.
    if blockchain.validate_blockchain():
        print("Blockchain bilkul sahi hai")
    
    else:
        print("Blockchain validate nahi hua hai , tampering of the data is detected!")

if __name__ == "__main__":
    main()
