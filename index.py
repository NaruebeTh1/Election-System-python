from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.asymmetric import padding
import hashlib

class Voter:
    def __init__(self, student_id):
        self.student_id = student_id
        self.selected_candidate = None
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

    def sign_vote(self, candidate):
        # Sign the selected candidate with the voter's private key
        signature = self.private_key.sign(
            f"{self.student_id}{candidate}".encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA512()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA512()
        )
        return signature

class ElectionSystem:
    def __init__(self):
        self.candidates = ['A', 'B', 'C']
        self.voters = []
        self.votes = []

    def add_voter(self, student_id, selected_candidate, signature):
        voter = Voter(student_id)
        voter.selected_candidate = selected_candidate

        # Simulate the signing process
        signature = voter.sign_vote(selected_candidate)

        # Verify voter identity and signature
        if self.verify_voter(voter, signature):
            self.voters.append(voter)
            self.votes.append(self.calculate_vote_hash())

    def verify_voter(self, voter, signature):
        # Verify the voter's identity and signature
        try:
            voter.public_key.verify(
                signature,
                f"{voter.student_id}{voter.selected_candidate}".encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA512()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA512()
            )
            return True
        except Exception as e:
            print(f"Verification failed: {e}")
            return False

    def calculate_vote_hash(self):
        # Concatenate voter data and calculate hash
        data_to_hash = ''.join([str(voter.student_id) + voter.selected_candidate for voter in self.voters])
        return hashlib.sha512(data_to_hash.encode()).hexdigest()

    def display_election_results(self):
        print("Election Results:")
        print("Student ID\tCandidate\tHash")
        last_index = len(self.votes) - 1
        for i, voter in enumerate(self.voters):
            if i == last_index:
                print(f"{voter.student_id}\t{voter.selected_candidate}\t\t{self.votes[i]}")
                break
            else:
                print(f"{voter.student_id}\t{voter.selected_candidate}\t\t ")

if __name__ == "__main__":
    election_system = ElectionSystem()

    while True:
        student_id = input("Enter student ID (or type 'exit' to finish): ")
        
        # ตรวจสอบว่าผู้ใช้ต้องการจะออกจากโปรแกรมหรือไม่
        if student_id.lower() == 'exit':
            break

        selected_candidate = input("Select candidate (A, B, C): ")
        signature = input("Enter signature: ")

        election_system.add_voter(student_id, selected_candidate, signature)

    # Display election results
    election_system.display_election_results()
