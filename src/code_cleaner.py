import ast

def clean_python_code(code_str: str) -> str:
    """
    使用 AST 解析 Python 代码，验证语法正确性，并剔除无用的文档注释 (Docstrings)。
    如果代码存在语法错误，则返回 None，以便流水线将其作为劣质数据过滤。
    """
    # 1. 判断空白
    if not code_str or not isinstance(code_str, str):
        return None
        
    try:
        # 2. 核心：尝试将字符串解析为 AST 树
        # 如果代码少了一个括号或有严重的语法错误，这里会直接给出 SyntaxError
        tree = ast.parse(code_str)
        
        # 3. 遍历语法树，寻找所有的模块、类和函数
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.Module)):
                # 如果这个节点内部有代码，并且第一行是一个纯字符串（这在 Python 中是 Docstring/多行注释）
                if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
                    if isinstance(node.body[0].value.value, str):
                        # 将这段无用的注释从语法树上去掉
                        node.body.pop(0)
                        
        # 4. 将修剪干净的语法树，重新转化为纯净的 Python 代码字符串
        cleaned_code = ast.unparse(tree)
        return cleaned_code
        
    except SyntaxError as e:
        # 捕获到语法错误，这是一段无法运行的烂代码
        print(f"剔除劣质代码！检测到语法错误: {e}")
        return None
    except Exception as e:
        # 捕获其他异常（确保流水线不会因为一条烂数据而中断崩溃）
        print(f"解析异常: {e}")
        return None

# --- 本地快速测试代码 ---
if __name__ == "__main__":
    # 构造一段极具迷惑性的脏代码：包含多行注释，以及字符串里带有假注释
    dirty_code = '''
def calculate_damage(attack, defense):
    """
    这是一个计算伤害的函数。
    大模型训练时不需要这段废话，因为我们要模型学习计算逻辑。
    """
    # 下面这一行不会被误删，因为 AST 知道它是个字符串，不是真的注释
    message = "这里的 # 不是注释" 
    return max(0, attack - defense)
    '''
    
    # 构造一段有语法错误的代码（少写了一个冒号）
    broken_code = '''
def heal(hp)
    return hp + 100
    '''
    
    print("【测试 1：清洗正常代码】")
    print("清洗前:\n", dirty_code.strip())
    print("-" * 30)
    print("清洗后:\n", clean_python_code(dirty_code))
    
    print("\n" + "="*40 + "\n")
    
    print("【测试 2：拦截语法错误的烂代码】")
    result = clean_python_code(broken_code)
    print("返回结果:", result)