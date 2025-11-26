class LZWCompressor:
    def __init__(self):
        self.reset_dictionary()
    
    def reset_dictionary(self):
        """Инициализация базового словаря ASCII символами"""
        self.dictionary = {}
        self.reverse_dict = {}
        # Добавляем все базовые символы
        for i in range(256):
            self.dictionary[chr(i)] = i
            self.reverse_dict[i] = chr(i)
        self.next_code = 256
    
    def compress(self, data):
        """Сжатие данных алгоритмом LZW"""
        self.reset_dictionary()
        result = []
        
        current = ""
        for char in data:
            current_plus_char = current + char
            if current_plus_char in self.dictionary:
                current = current_plus_char
            else:
                # Выводим код для текущей строки
                result.append(self.dictionary[current])
                # Добавляем новую строку в словарь
                self.dictionary[current_plus_char] = self.next_code
                self.next_code += 1
                current = char
        
        # Выводим последний код
        if current:
            result.append(self.dictionary[current])
        
        return result
    
    def decompress(self, compressed_data):
        """Распаковка данных алгоритмом LZW"""
        self.reset_dictionary()
        
        if not compressed_data:
            return ""
        
        # Первый код
        prev_code = compressed_data[0]
        result = self.reverse_dict[prev_code]
        current = result
        
        for code in compressed_data[1:]:
            if code in self.reverse_dict:
                entry = self.reverse_dict[code]
            elif code == self.next_code:
                entry = current + current[0]
            else:
                raise ValueError(f"Некорректный код: {code}")
            
            result += entry
            
            # Добавляем новую запись в словарь
            self.reverse_dict[self.next_code] = current + entry[0]
            self.next_code += 1
            
            current = entry
        
        return result

    def compression_ratio(self, original, compressed):
        """Расчет коэффициента сжатия"""
        original_size = len(original) * 8  # биты
        compressed_size = len(compressed) * 12  # предполагаем 12 бит на код
        return original_size / compressed_size

def demonstrate_lzw():
    """Демонстрация работы алгоритма LZW"""
    lzw = LZWCompressor()
    
    test_cases = [
        "ABABABA",
        "TOBEORNOTTOBEORTOBEORNOT",
        "AAAAAAA",
        "Hello, World!",
        "ABABABABABABABAB"
    ]
    
    print("ДЕМОНСТРАЦИЯ АЛГОРИТМА LZW")
    print("=" * 50)
    
    for i, test_data in enumerate(test_cases, 1):
        print(f"\nТест {i}: '{test_data}'")
        print("-" * 30)
        
        # Сжатие
        compressed = lzw.compress(test_data)
        print(f"Исходные данные: {test_data}")
        print(f"Длина исходных: {len(test_data)} символов")
        print(f"Сжатые коды: {compressed}")
        print(f"Количество кодов: {len(compressed)}")
        
        # Распаковка
        decompressed = lzw.decompress(compressed)
        print(f"Распаковано: '{decompressed}'")
        
        # Проверка
        if test_data == decompressed:
            print("✓ Сжатие/распаковка успешны")
        else:
            print("✗ Ошибка сжатия/распаковки")
        
        # Коэффициент сжатия
        ratio = lzw.compression_ratio(test_data, compressed)
        print(f"Коэффициент сжатия: {ratio:.2f}:1")
        
        # Детализация процесса для первого теста
        if i == 1:
            print("\nДетальный процесс сжатия 'ABABABA':")
            print("Словарь в процессе:")
            detailed_compression(lzw, test_data)

def detailed_compression(lzw, data):
    """Детальное отображение процесса сжатия"""
    lzw.reset_dictionary()
    
    current = ""
    step = 1
    
    print("\nШаг | Текущая | Символ | Новая строка | Вывод | Новый код")
    print("-" * 65)
    
    for char in data:
        current_plus_char = current + char
        if current_plus_char in lzw.dictionary:
            current = current_plus_char
            print(f"{step:3} | {current:7} | {char:6} | {'':11} | {'':5} |")
        else:
            output = lzw.dictionary[current]
            new_code = lzw.next_code
            print(f"{step:3} | {current:7} | {char:6} | {current_plus_char:11} | {output:5} | {new_code:8}")
            
            lzw.dictionary[current_plus_char] = new_code
            lzw.next_code += 1
            current = char
        step += 1
    
    # Последний вывод
    if current:
        output = lzw.dictionary[current]
        print(f"{step:3} | {current:7} | {'':6} | {'':11} | {output:5} |")

def analyze_compression():
    """Анализ эффективности сжатия разных типов данных"""
    lzw = LZWCompressor()
    
    test_patterns = {
        "Повторяющийся паттерн": "ABABABABABABABABABABABAB",
        "Одинаковые символы": "AAAAAAAAAAAAAAAAAAAA",
        "Случайные символы": "XYZPQRMNOLKJIHGFEDCBA",
        "Текст с повторениями": "hello hello world world test test",
        "Короткая строка": "ABC",
        "Длинная повторяющаяся": "A" * 50
    }
    
    print("\nАНАЛИЗ ЭФФЕКТИВНОСТИ СЖАТИЯ")
    print("=" * 60)
    print(f"{'Тип данных':<25} {'Исходный размер':<15} {'Сжатый размер':<15} {'Коэффициент':<12}")
    print("-" * 60)
    
    for description, data in test_patterns.items():
        compressed = lzw.compress(data)
        original_size = len(data)
        compressed_size = len(compressed)
        ratio = original_size / compressed_size if compressed_size > 0 else 0
        
        print(f"{description:<25} {original_size:<15} {compressed_size:<15} {ratio:>8.2f}:1")

def interactive_demo():
    """Интерактивная демонстрация"""
    lzw = LZWCompressor()
    
    print("\nИНТЕРАКТИВНАЯ ДЕМОНСТРАЦИЯ LZW")
    print("=" * 40)
    
    while True:
        user_input = input("\nВведите строку для сжатия (или 'exit' для выхода): ")
        
        if user_input.lower() == 'exit':
            break
        
        if not user_input:
            continue
        
        # Сжатие
        compressed = lzw.compress(user_input)
        decompressed = lzw.decompress(compressed)
        
        print(f"\nИсходная строка: '{user_input}'")
        print(f"Длина: {len(user_input)} символов")
        print(f"Сжатые коды: {compressed}")
        print(f"Количество кодов: {len(compressed)}")
        print(f"Распакованная строка: '{decompressed}'")
        
        # Эффективность
        if len(compressed) > 0:
            efficiency = (1 - len(compressed) / len(user_input)) * 100
            print(f"Эффективность сжатия: {efficiency:+.1f}%")
        
        if user_input == decompressed:
            print("✓ Целостность данных сохранена")
        else:
            print("✗ Ошибка! Данные повреждены")

if __name__ == "__main__":
    # Запуск демонстраций
    demonstrate_lzw()
    analyze_compression()
    interactive_demo()