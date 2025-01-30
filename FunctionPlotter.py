import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from sympy import symbols, sympify, solve

class FunctionPlotter:
    def __init__(self, root):
        """
        初始化函数图像绘制计算器
        :param root: Tkinter根窗口
        """
        self.root = root
        self.root.title("函数图像绘制计算器")
        self.root.geometry("800x600")

        # 存储用户输入的函数表达式
        self.functions = []
        # 默认的X和Y范围
        self.x_range = (-10, 10)
        self.y_range = (-10, 10)
        # 生成X值的数组
        self.x = np.linspace(self.x_range[0], self.x_range[1], 1000)

        # 创建输入区域
        self.create_widgets()
        # 创建绘图区域
        self.create_plot_area()

    def create_widgets(self):
        """
        创建输入区域的控件
        """
        input_frame = tk.Frame(self.root)
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # 创建函数表达式输入框
        tk.Label(input_frame, text="函数表达式:").grid(row=0, column=0, sticky=tk.W)
        self.function_entry = tk.Entry(input_frame, width=50)
        self.function_entry.grid(row=0, column=1, padx=5)

        # 创建添加函数按钮
        add_button = tk.Button(input_frame, text="添加函数", command=self.add_function)
        add_button.grid(row=0, column=2, padx=5)

        # 创建删除函数按钮
        remove_button = tk.Button(input_frame, text="删除函数", command=self.remove_function)
        remove_button.grid(row=0, column=3, padx=5)

        # 创建绘制图形按钮
        plot_button = tk.Button(input_frame, text="绘制图形", command=self.plot_functions)
        plot_button.grid(row=0, column=4, padx=5)

        # 创建说明按钮
        help_button = tk.Button(input_frame, text="说明", command=self.show_help)
        help_button.grid(row=0, column=5, padx=5)

        # 创建函数列表显示框
        self.function_list = tk.Listbox(input_frame, width=50, height=5)
        self.function_list.grid(row=1, column=0, columnspan=6, pady=10)

        # 创建X轴范围输入框
        tk.Label(input_frame, text="X轴范围:").grid(row=2, column=0, sticky=tk.W)
        self.x_range_entry = tk.Entry(input_frame, width=20)
        self.x_range_entry.grid(row=2, column=1, padx=5)
        self.x_range_entry.insert(0, "-10, 10")  # 默认X范围

        # 创建Y轴范围输入框
        tk.Label(input_frame, text="Y轴范围:").grid(row=2, column=2, sticky=tk.W)
        self.y_range_entry = tk.Entry(input_frame, width=20)
        self.y_range_entry.grid(row=2, column=3, padx=5)
        self.y_range_entry.insert(0, "-10, 10")  # 默认Y范围

    def create_plot_area(self):
        """
        创建绘图区域
        """
        # 创建Matplotlib图形和坐标轴
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        # 设置坐标轴标签
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        # 显示网格
        self.ax.grid(True)
        # 绘制X和Y轴
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)
        # 将Matplotlib图形嵌入Tkinter窗口
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def add_function(self):
        """
        添加函数到列表
        """
        function_str = self.function_entry.get()
        if function_str:
            self.functions.append(function_str)
            self.function_list.insert(tk.END, function_str)
            self.function_entry.delete(0, tk.END)

    def remove_function(self):
        """
        从列表中删除选中的函数
        """
        selected_index = self.function_list.curselection()
        if selected_index:
            self.functions.pop(selected_index[0])
            self.function_list.delete(selected_index[0])

    def plot_functions(self):
        """
        绘制所有函数的图像并计算交点
        """
        # 获取用户输入的X和Y范围
        try:
            x_min, x_max = map(float, self.x_range_entry.get().split(","))
            y_min, y_max = map(float, self.y_range_entry.get().split(","))
            self.x_range = (x_min, x_max)
            self.y_range = (y_min, y_max)
            self.x = np.linspace(x_min, x_max, 1000)
        except ValueError:
            messagebox.showerror("输入错误", "X轴和Y轴范围格式不正确，请使用逗号分隔的两个数字，例如：-10, 10")
            return

        # 清除之前的图形
        self.ax.clear()
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.grid(True)
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)

        # 设置坐标轴范围
        self.ax.set_xlim(self.x_range)
        self.ax.set_ylim(self.y_range)

        # 定义符号变量x
        x = symbols('x')
        for i, func_str in enumerate(self.functions):
            try:
                # 将字符串表达式转换为SymPy表达式
                func = sympify(func_str)
                # 计算Y值
                y = [func.subs(x, val) for val in self.x]
                # 绘制函数图像
                self.ax.plot(self.x, y, label=f"f{x} = {func_str}")
            except Exception as e:
                messagebox.showerror("绘图错误", f"无法绘制函数 {func_str}: {e}")

        # 计算交点
        for i in range(len(self.functions)):
            for j in range(i + 1, len(self.functions)):
                try:
                    # 将字符串表达式转换为SymPy表达式
                    func1 = sympify(self.functions[i])
                    func2 = sympify(self.functions[j])
                    # 计算交点
                    intersections = solve(func1 - func2, x)
                    for intersect in intersections:
                        if intersect.is_real:
                            x_intersect = float(intersect)
                            y_intersect = func1.subs(x, x_intersect)
                            # 在图形上标记交点
                            self.ax.plot(x_intersect, y_intersect, 'ro')
                            # 在交点旁边显示坐标
                            self.ax.text(x_intersect, y_intersect, f"({x_intersect:.2f}, {y_intersect:.2f})",
                                         fontsize=9, verticalalignment='bottom')
                except Exception as e:
                    messagebox.showerror("交点计算错误", f"无法计算函数 {self.functions[i]} 和 {self.functions[j]} 的交点: {e}")

        # 显示图例
        self.ax.legend()
        # 刷新图形
        self.canvas.draw()

    def show_help(self):
        """
        显示说明窗口
        """
        help_window = tk.Toplevel(self.root)
        help_window.title("使用说明")
        help_window.geometry("1000x400")

        help_text = """
        使用说明：
        1. 在“函数表达式”框中输入函数表达式，例如：x**2(这种写法为适应编写语言Python中的写法，实际意思即为x的2次方) \n\t   或 math.sin(x) (同样为适应编写语言Python中的写法，如果直接写sin等报错，可以选择加上\"math.\")。\n
        2. 输入的函数如y = 3x + 5，输入时无需输入y = ，仅输入3*x+5，注意：此应用无法识别省略*的写法.\n
        3. 点击“添加函数”按钮将函数添加到列表中。\n
        4. 在“X轴范围”和“Y轴范围”框中输入范围，例如：-10, 10。\n
        5. 点击“绘制图形”按钮绘制所有函数的图像并计算交点。\n
        6. 点击“删除函数”按钮从列表中删除选中的函数。\n
        7. 点击“说明”按钮查看使用说明。
        """
        help_label = tk.Label(help_window, text=help_text, font=("宋体", 12), justify="left")
        help_label.pack(pady=20, padx=20, fill="both")

        close_button = tk.Button(help_window, text="关闭", command=help_window.destroy)
        close_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FunctionPlotter(root)
    root.mainloop()
