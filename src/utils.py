def print_list_tuple_vacancies(vacancies):
    for vacancy in vacancies:
        if vacancy[1] != 0:
            print(f"Название: {vacancy[0]}, зарплата: {vacancy[1]}\nСсылка: {vacancy[2]}")
        else:
            print(f"Название: {vacancy[0]}, зарплата: не указана.\nСсылка: {vacancy[2]}")
