import tkinter as tk

root = tk.Tk()
S = tk.Scrollbar(root)
T = tk.Text(root, height=4, width=50)
S.pack(side="right", fill="y")
T.pack(side="left", fill="y")
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
quote = """HAMLET: To be, or not to be--that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune
Or to take arms against a sea of troubles
And by opposing end them. To die, to sleep--
No more--and by a sleep to say we end
The heartache, and the thousand natural shocks
That flesh is heir to. 'Tis a consummation
Devoutly to be wished."""
T.insert("end", quote)
root.mainloop()