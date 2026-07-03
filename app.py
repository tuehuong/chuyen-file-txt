"""
PHAN MEM CHINH SUA DU LIEU TU DONG
----------------------------------
Doc file .txt dau vao (moi dong la 1 muc du lieu), tu dong bien doi
theo dung logic cong thuc cot B trong file Excel goc, roi ghi ra
file .txt dau ra.

Cach dung:
  - Bam dup vao file de mo giao dien (can cai Python, khong can
    cai them thu vien nao vi chi dung thu vien co san).
  - Hoac chay dong lenh:  python app.py input.txt output.txt
"""

import sys
import os


def transform_line(a: str) -> str:
    """Tai tao chinh xac cong thuc cot B trong file Excel goc."""
    if a == "":
        return ""

    # F: co chua "Hoat dong" khong (khong phan biet hoa/thuong)
    f = 1 if "hoạt động" in a.lower() else 0

    # G: vi tri dau phay dau tien (1-based), 0 neu khong co
    comma_idx = a.find(",")
    g = comma_idx + 1 if comma_idx != -1 else 0

    if g == 0:
        h = ""
        i = ""
    else:
        h = a[:g - 1]          # phan truoc dau phay
        i = a[g - 1:]          # phan tu dau phay tro di

    # J: so dau cach trong h
    j = h.count(" ")

    if j < 1:
        k = 0
    else:
        positions = [idx + 1 for idx, ch in enumerate(h) if ch == " "]
        k = positions[j - 1]  # dau cach thu J (cuoi cung)

    if j < 2:
        l = 0
    else:
        positions = [idx + 1 for idx, ch in enumerate(h) if ch == " "]
        l = positions[j - 2]  # dau cach thu J-1 (ap chot)

    m = "" if l == 0 else h[l:k - 1]      # tu ap chot
    n = "" if k == 0 else h[k:]           # tu cuoi cung
    o = "" if l == 0 else h[:l]           # phan truoc (gom ca dau cach ap chot)

    if f == 1 and g > 0 and j >= 2:
        return f'{o}{n} ({m}){i}'
    else:
        return a


def process_file(input_path: str, output_path: str) -> int:
    with open(input_path, "r", encoding="utf-8-sig") as fin:
        lines = fin.read().splitlines()

    results = [transform_line(line) for line in lines]

    with open(output_path, "w", encoding="utf-8") as fout:
        fout.write("\n".join(results))

    return len(results)


def run_cli(argv):
    if len(argv) != 3:
        print("Cach dung: python app.py input.txt output.txt")
        sys.exit(1)
    n = process_file(argv[1], argv[2])
    print(f"Da xu ly {n} dong. Ket qua luu tai: {argv[2]}")


def run_gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox

    root = tk.Tk()
    root.title("Phan mem chinh sua du lieu tu dong")
    root.geometry("520x260")
    root.resizable(False, False)

    input_path_var = tk.StringVar()
    output_path_var = tk.StringVar()
    status_var = tk.StringVar(value="Chua chon file.")

    def choose_input():
        path = filedialog.askopenfilename(
            title="Chon file .txt dau vao",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if path:
            input_path_var.set(path)
            base, ext = os.path.splitext(path)
            output_path_var.set(f"{base}_ketqua.txt")
            status_var.set("Da chon file dau vao. San sang xu ly.")

    def choose_output():
        path = filedialog.asksaveasfilename(
            title="Chon noi luu file ket qua",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if path:
            output_path_var.set(path)

    def do_process():
        inp = input_path_var.get().strip()
        out = output_path_var.get().strip()
        if not inp:
            messagebox.showwarning("Thieu file", "Vui long chon file .txt dau vao truoc.")
            return
        if not out:
            messagebox.showwarning("Thieu noi luu", "Vui long chon noi luu file ket qua.")
            return
        try:
            n = process_file(inp, out)
            status_var.set(f"Hoan tat! Da xu ly {n} dong.")
            messagebox.showinfo("Thanh cong", f"Da xu ly {n} dong.\nFile ket qua:\n{out}")
        except Exception as e:
            status_var.set("Co loi xay ra.")
            messagebox.showerror("Loi", f"Khong the xu ly file:\n{e}")

    tk.Label(root, text="Phan mem chinh sua du lieu tu dong", font=("Segoe UI", 13, "bold")).pack(pady=(15, 5))
    tk.Label(root, text="(giu nguyen logic cong thuc cot B trong file Excel goc)", font=("Segoe UI", 9)).pack()

    frame1 = tk.Frame(root)
    frame1.pack(pady=(20, 5), padx=20, fill="x")
    tk.Button(frame1, text="1. Chon file .txt dau vao", width=28, command=choose_input).pack(side="left")
    tk.Entry(frame1, textvariable=input_path_var, width=30, state="readonly").pack(side="left", padx=8)

    frame2 = tk.Frame(root)
    frame2.pack(pady=5, padx=20, fill="x")
    tk.Button(frame2, text="2. Chon noi luu file ket qua", width=28, command=choose_output).pack(side="left")
    tk.Entry(frame2, textvariable=output_path_var, width=30, state="readonly").pack(side="left", padx=8)

    tk.Button(root, text="3. XU LY", width=20, height=2, bg="#2e7d32", fg="white",
              font=("Segoe UI", 10, "bold"), command=do_process).pack(pady=20)

    tk.Label(root, textvariable=status_var, fg="#555").pack()

    root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_cli(sys.argv)
    else:
        run_gui()
