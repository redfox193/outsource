### Гончаров Сергей Витальевич, 3 курс, 11 группа

# Шаг 1
Справочники хранят информацию организации, которая занимаетса выполнением проектов на аутсорс.
### Справочник "Project"

| Поле                | Тип данных              | Описание                                                   |
|---------------------|-------------------------|-----------------------------------------------------------|
| **id**             | Число                   | Уникальный идентификатор проекта.                         |
| **name**     | Текст                   | Краткое название проекта.                                 |
| **description** | Текст                | Подробное описание цели и содержания проекта.             |
| **budget**          | Число с фиксированной запятой | Общая сумма, выделенная на проект.                        |
| **deadline**        | Дата                    | Крайний срок выполнения проекта.                          |

---

### Справочник "Employee"

| Поле                 | Тип данных              | Описание                                                   |
|----------------------|-------------------------|-----------------------------------------------------------|
| **id**              | Число                   | Уникальный идентификатор сотрудника.                      |
| **fullName**        | Текст                   | Полное имя сотрудника.                                    |
| **position**        | Текст                   | Роль или позиция сотрудника в компании.                   |
| **projectId**       | Ссылка на справочник    | ID проекта из справочника "Project", к которому относится сотрудник. |
| **completedProjects** | Целое число       | Количество успешных проектов, которые выполнил сотрудник. |

---

### Пример связи:
1. Поле **"projectID"** в справочнике "Employee" ссылается на поле **ID** справочника "Project". Поле _NOT NULL_

# Шаг 2
#### Будем использовать PostgreSQL <br>
![diag](https://github.com/redfox193/outsource/blob/main/diag.png)
```sql
INSERT INTO Project (ID, ProjectName, ProjectDescription, Budget, Deadline)
VALUES
    (1, 'Проект A', 'Описание проекта A', 1000000.50, '2025-12-31'),
    (2, 'Проект B', 'Описание проекта B', 500000.50, '2026-06-30');

INSERT INTO Employee (ID, FullName, Position, ProjectID, SuccessfulProjectsCount)
VALUES
    (1, 'Гончаров Сергей Витальевич', 'Менеджер', 1, 5),
    (2, 'Довгий Александр Сергеевич', 'Разработчик', 2, 3),
    (3, 'Игнатчик Ульяна Сергеевна', 'Тестировщик', 2, 4);
```
