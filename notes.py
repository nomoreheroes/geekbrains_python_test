import json
import os.path
import datetime
import os


class Notes:
    filename = "data.json"

    def __init__(self):
        if os.path.isfile(self.filename):
            with open(self.filename,"r") as fp:
                self._list = json.load(fp)
        else:
            self._list = []
        self._current_note = len(self._list) - 1

    def appendNote(self,note):
        self._list.append(note)
        self.save()

    def save(self):
        with open(self.filename,"w+") as fp:
            json.dump(self._list, fp)

    def get_all_notes(self):
        return self.get_notes_by_ind(0,self.get_length()-1)
    
    def get_notes_by_ind(self,start,end):
        return self._list[start:end+1]

    def delete(self,ind):
        del self._list[ind]
        self.save()

    def edit(self, ind, new_note):
        self._list[ind] = new_note
        self.save()

    def get_length(self):
        return len(self._list)
    
    def get(self, num):
        return self._list[num]

class App:

    def __init__(self):
        self.notes = Notes()

    def show_list(self,mode,start=None,end=None):
        if mode == "all":
            for num,note in enumerate(self.notes.get_all_notes()):
                print("{0}№{1} от {2}{3}: {4}...(показать - '{1}'){5}".format('\033[4m',num,
                                                                     note["creation_date"],
                                                                          ", изменено {0}".format(note["change_date"]) if note["creation_date"] != note["change_date"] else "", 
                                                                          note["header"],'\033[0m'))
        elif mode == "date" and start is not None:
            dt1 = datetime.datetime.strptime(command, '%d.%m.%Y')
            for num,note in enumerate(self.notes.get_all_notes()):
                dt2 = datetime.datetime.strptime(note["creation_date"], '%d.%m.%Y')
                if dt2 == dt1:
                    print("{0}№{1} от {2}{3}: {4}...(показать - '{1}'){5}".format('\033[4m',num,
                                                                     note["creation_date"],
                                                                          ", изменено {0}".format(note["change_date"]) if note["creation_date"] != note["change_date"] else "", 
                                                                          note["header"],'\033[0m'))

        elif mode == "slice" and start is not None and end is not None:
            for num, note in enumerate(self.notes.get_notes_by_ind(start,end)):
                print("{0}№{1} от {2}{3}: {4}...(показать - '{1}'){5}".format('\033[4m',num+start,
                                                                     note["creation_date"],
                                                                          ", изменено {0}".format(note["change_date"]) if note["creation_date"] != note["change_date"] else "", 
                                                                          note["header"],'\033[0m')) 
            

    def show(self,num = None):
        if num == None:
            if self.notes.get_length() == 0:
                print("Пока в приложении нет заметок")
                return
            else:
                num = self.notes.get_length()-1
        if num < 0:
            num = 0
        if num >= self.notes.get_length():
            num = self.notes.get_length()-1
        if int(num-1) > 0:
            prev_note = self.notes.get(num-1)
            print("{0}Предыдущая заметка №{1} от {2}{3}: {4}...(показать - '<'){5}".format('\033[4m',num-1,
                                                                     prev_note["creation_date"],
                                                                          ", изменено {0}".format(prev_note["change_date"]) if prev_note["creation_date"] != prev_note["change_date"] else "", 
                                                                          prev_note["header"],'\033[0m'))
            print("----------------------------------------")
        note = self.notes.get(num)
        print("{0}ЗАМЕТКА №{1} ОТ {2}{3}{4}".format('\033[7m',num, note["creation_date"], ", изменено {0}".format(note["change_date"]) if note["creation_date"] != note["change_date"] else "",'\033[0m'))
        print("{0}{1}{2}".format('\033[7m',note["text"],'\033[0m'))
        print("----------------------------------------")
        if(int(num+1) < self.notes.get_length()):
            next_note = self.notes.get(num+1)
            print("{0}Следующая заметка №{1} от {2}{3}: {4}...(показать - '>'){5}".format('\033[4m',num+1,
                                                                     next_note["creation_date"],
                                                                          ", изменено {0}".format(next_note["change_date"]) if next_note["creation_date"] != next_note["change_date"] else "", 
                                                                          next_note["header"],'\033[0m'))


if __name__ == '__main__':
    os.system('color')
    app = App()
    print("Приветствуем вас в приложении для хранения заметок.")
    help = """
Основные команды:
1. > - следующая заметка
2. < - предыдущая заметка
3. add - добавить заметку в список
4. all - напечатать весь список заметок
5. N-M - напечатать список заметок с номера N по М
5. dd.mm.YYYY - напечатать список заметок на определенную дату
6. N - показать заметку с номером N
7. edit N "текст заметки" - редактировать заметку с номером N
8. delete N - удалить заметку
9. quit - выйти из приложения
"""
print(help)
x = input("Продолжить?(y/n)")

if x == "y":
    current_note = app.notes.get_length()-1
    app.show()
    while(True):
        command = input("Введите команду:\n")
        if command == "quit":
            break
        elif command == "add":
            text = input("Введите текст заметки:\n")
            x = input("Сохранить заметку? (y/n)")
            if x == "y":
                dt = datetime.datetime.now()
                dt = "{0}.{1}.{2}".format(dt.day,dt.month,dt.year)
                note = {
                    "text":text,
                    "header":" ".join(text.split(" ")[:5]),
                    "creation_date":dt,
                    "change_date":dt
                }
                app.notes.appendNote(note)
            app.show()
        elif command == "<":
            app.show(current_note-1)
            current_note -=1
        elif command == ">":
            app.show(current_note+1)
            current_note+=1
        elif command == "all":
            app.show_list("all")
        elif command.isnumeric():
            app.show(int(command))
        elif "-" in command:
            params = command.split("-")
            start = int(params[0])
            end = int(params[1])
            app.show_list("slice",start,end)
        elif "delete" in command:
            params = command.split(" ")
            num = int(params[1])
            x = input("Удалить заметку с номером {0}? (y/n)".format(num))
            if x == "y":
                app.notes.delete(num)
                print("Заметка удалена.")
        elif "edit" in command:
            params = command.split(" ")
            num = int(params[1])
            note = app.notes.get(num)
            print("Текст заметки для вставки/копирования: {0}".format(note["text"]))
            new_text = input("Введите новый текст заметки:\n")
            note["text"] = new_text                
            dt = datetime.datetime.now()
            note["date_changed"] = "{0}.{1}.{2}".format(dt.day,dt.month,dt.year)
            note["header"] = " ".join(new_text.split(" ")[:5])
            app.notes.edit(num,note)
            print("Заметка отредактирована")
        else:
            try:
                dt = datetime.datetime.strptime(command, '%d.%m.%Y')
                if isinstance(dt,datetime.datetime):
                    app.show_list("date",command)
            except ValueError:
                pass




    