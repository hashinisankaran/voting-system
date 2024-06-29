import tkinter as tk
from tkinter import messagebox, filedialog
import hashlib
import datetime as date

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        hash_str = (str(self.index) + 
                    str(self.timestamp) + 
                    str(self.data) + 
                    str(self.previous_hash)).encode('utf-8')
        sha.update(hash_str)
        return sha.hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, date.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True


class VotingSystem:
    def __init__(self):
        self.blockchain = Blockchain()
        self.candidates = {}
        self.votes = []

    def add_candidate(self, candidate_name):
        if candidate_name not in self.candidates:
            self.candidates[candidate_name] = 0

    def vote(self, voter_name, voter_id, candidate_name):
        if candidate_name in self.candidates:
            vote_data = {'voter_name': voter_name, 'voter_id': voter_id, 'candidate': candidate_name}
            new_block = Block(len(self.blockchain.chain), date.datetime.now(), vote_data, self.blockchain.get_latest_block().hash)
            self.blockchain.add_block(new_block)
            self.candidates[candidate_name] += 1
            self.votes.append(vote_data)
            return True
        else:
            return False

    def get_candidates(self):
        return self.candidates

    def get_votes(self):
        return self.votes


class VotingApp:
    def __init__(self, root):
        self.root = root
        # Maximize window to full screen
        self.root.attributes('-fullscreen', True)
        self.root.title("Blockchain Voting System")

        self.voting_system = VotingSystem()

        # Create main frame to hold all widgets
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Candidate entry and add button
        candidate_frame = tk.Frame(main_frame)
        candidate_frame.pack(pady=(50, 10))

        self.label_candidate = tk.Label(candidate_frame, text="Candidate:", font=('Helvetica', 24))
        self.label_candidate.grid(row=0, column=0, padx=20, pady=10)

        self.entry_candidate = tk.Entry(candidate_frame, font=('Helvetica', 24), width=30)
        self.entry_candidate.grid(row=0, column=1, padx=20, pady=10)

        self.button_add_candidate = tk.Button(candidate_frame, text="Add Candidate", font=('Helvetica', 16), command=self.add_candidate)
        self.button_add_candidate.grid(row=0, column=2, padx=20, pady=10)

        # Voter name entry and photo upload
        voter_frame = tk.Frame(main_frame)
        voter_frame.pack(pady=10)

        self.label_voter_name = tk.Label(voter_frame, text="Voter Name:", font=('Helvetica', 24))
        self.label_voter_name.grid(row=0, column=0, padx=20, pady=10)

        self.entry_voter_name = tk.Entry(voter_frame, font=('Helvetica', 24), width=30)
        self.entry_voter_name.grid(row=0, column=1, padx=20, pady=10)

        self.label_voter_id = tk.Label(voter_frame, text="Voter ID:", font=('Helvetica', 24))
        self.label_voter_id.grid(row=1, column=0, padx=20, pady=10)

        self.entry_voter_id = tk.Entry(voter_frame, font=('Helvetica', 24), width=30)
        self.entry_voter_id.grid(row=1, column=1, padx=20, pady=10)

        self.label_photo = tk.Label(voter_frame, text="Voter Photo:", font=('Helvetica', 24))
        self.label_photo.grid(row=2, column=0, padx=20, pady=10)

        self.button_upload_photo = tk.Button(voter_frame, text="Upload Photo", font=('Helvetica', 16), command=self.upload_photo)
        self.button_upload_photo.grid(row=2, column=1, padx=20, pady=10)

        self.photo_path = None  # Variable to store uploaded photo path

        # Vote for candidate selection
        vote_frame = tk.Frame(main_frame)
        vote_frame.pack(pady=10)

        self.label_vote_candidate = tk.Label(vote_frame, text="Vote for Candidate:", font=('Helvetica', 24))
        self.label_vote_candidate.grid(row=0, column=0, padx=20, pady=10)

        self.vote_options = tk.StringVar()
        self.vote_options.set("")  # Default value

        self.candidate_listbox = tk.OptionMenu(vote_frame, self.vote_options, "")
        self.candidate_listbox.config(width=27, font=('Helvetica', 24))
        self.candidate_listbox.grid(row=0, column=1, padx=20, pady=10)

        self.button_vote = tk.Button(vote_frame, text="Vote", font=('Helvetica', 16), command=self.process_vote)
        self.button_vote.grid(row=0, column=2, padx=20, pady=10)

        # Results display
        results_frame = tk.Frame(main_frame)
        results_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=(50, 0))

        self.label_results = tk.Label(results_frame, text="Results:", font=('Helvetica', 32))
        self.label_results.pack(pady=(0, 20))

        self.text_results = tk.Text(results_frame, height=10, width=50, font=('Helvetica', 18))
        self.text_results.pack(expand=True, fill=tk.BOTH)

        self.display_results()

    def add_candidate(self):
        candidate_name = self.entry_candidate.get().strip()
        if candidate_name:
            self.voting_system.add_candidate(candidate_name)
            self.update_candidate_listbox()
            self.entry_candidate.delete(0, 'end')
            messagebox.showinfo("Success", f"Candidate '{candidate_name}' added successfully!")
        else:
            messagebox.showerror("Error", "Please enter a candidate name.")

    def upload_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.photo_path = file_path
            messagebox.showinfo("Success", "Photo uploaded successfully!")
        else:
            messagebox.showerror("Error", "No file selected.")

    def process_vote(self):
        voter_name = self.entry_voter_name.get().strip()
        voter_id = self.entry_voter_id.get().strip()
        candidate_name = self.vote_options.get()
        if voter_name and voter_id and candidate_name:
            if self.voting_system.vote(voter_name, voter_id, candidate_name):
                voter_slip = f"Vote successfully recorded!\n\nVoter Name: {voter_name}\nVoter ID: {voter_id}\nCandidate Voted: {candidate_name}"
                messagebox.showinfo("Success", voter_slip)
            else:
                messagebox.showerror("Error", f"{candidate_name} is not a valid candidate.")
            self.display_results()
            self.entry_voter_name.delete(0, 'end')
            self.entry_voter_id.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Please enter voter name, voter ID, and select a candidate.")

    def update_candidate_listbox(self):
        self.candidate_listbox['menu'].delete(0, 'end')
        for candidate in self.voting_system.get_candidates().keys():
            self.candidate_listbox['menu'].add_command(label=candidate, command=tk._setit(self.vote_options, candidate))

    def display_results(self):
        self.text_results.delete('1.0', tk.END)
        results = "Candidate Votes:\n"
        candidates = self.voting_system.get_candidates()
        for candidate, votes in candidates.items():
            results += f"{candidate}: {votes} votes\n"
        self.text_results.insert(tk.END, results)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = VotingApp(root)
    root.mainloop()
