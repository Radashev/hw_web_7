from sqlalchemy import func, desc, select, and_
from conf.models import Grade, Student, Group, Subject, Teacher
from conf.db import session

import argparse


def create_teacher(name):
    # Логіка для створення вчителя
    teacher = Teacher(name=name)
    session.add(teacher)
    session.commit()

def list_teachers():
    # Логіка для відображення списку вчителів
    teachers = session.query(Teacher).all()
    for teacher in teachers:
        print(teacher.name)

def update_teacher(id, name):
    # Логіка для оновлення даних вчителя з певним id
    teacher = Teacher.query.get(id)
    if teacher:
        teacher.name = name
        session.commit()

def remove_teacher(id):
    # Логіка для видалення вчителя з певним id
    teacher = Teacher.query.get(id)
    if teacher:
        session.delete(teacher)
        session.commit()


def main():
    parser = argparse.ArgumentParser(description='CRUD operations with database')
    parser.add_argument('-a', '--action', choices=['create', 'list', 'update', 'remove'], help='Action to perform', required=True)
    parser.add_argument('-m', '--model', choices=['Teacher', 'Group'], help='Model to operate on', required=True)
    parser.add_argument('--id', type=int, help='ID of the record for update or remove actions')
    parser.add_argument('--name', help='Name for creating or updating records')  # Додано аргумент для імені
    args = parser.parse_args()

    if args.action == 'create':
        if args.model == 'Teacher' and args.name:
            create_teacher(args.name)
        elif args.model == 'Group' and args.name:
            # Додаткові функції для створення групи
            pass
    elif args.action == 'list':
        if args.model == 'Teacher':
            list_teachers()
        elif args.model == 'Group':
            # Додаткові функції для відображення списку груп
            pass
    elif args.action == 'update':
        if args.model == 'Teacher' and args.id and args.name:
            update_teacher(args.id, args.name)
        elif args.model == 'Group' and args.id and args.name:
            # Додаткові функції для оновлення групи
            pass
    elif args.action == 'remove':
        if args.model == 'Teacher' and args.id:
            remove_teacher(args.id)
        elif args.model == 'Group' and args.id:
            # Додаткові функції для видалення групи
            pass

def select_01():
    """
    SELECT students.id, students.name, ROUND(AVG(grades.grade), 2) AS average_grade
        FROM students
        JOIN grades ON students.id = grades.student_id
        GROUP BY students.id, students.name
        ORDER BY average_grade DESC
        LIMIT 5;
    """
    result = (
        session.query(
            Student.id,
            Student.name,
            func.round(func.avg(Grade.grade), 2).label('average_grade')
        )
        .join(Grade, Student.id == Grade.student_id)
        .group_by(Student.id, Student.name)
        .order_by(desc('average_grade'))
        .limit(5)
        .all()
    )
    return result

def select_02():
    """
    SELECT s.name AS student_name, ROUND(AVG(g.grade), 2) AS average_grade
        FROM students s
        JOIN grades g ON s.id = g.student_id
        WHERE g.subject_id = 1
        GROUP BY s.id, s.name
        ORDER BY average_grade DESC
        LIMIT 1;
    """
    result = (
        session.query(
            Student.id,
            Student.name,
            func.round(func.avg(Grade.grade), 2).label('average_grade')
        )
        .join(Grade, Student.id == Grade.student_id)
        .filter(Grade.subjects_id == 1)  # Використовуйте subjects_id
        .group_by(Student.id, Student.name)
        .order_by(desc('average_grade'))
        .limit(1)
        .all()
    )
    return result

def select_03():
    """
    SELECT g.name AS group_name, ROUND(AVG(gr.grade), 2) AS average_grade
        FROM groups_backup g
        JOIN students s ON g.id = s.group_id
        JOIN grades gr ON s.id = gr.student_id
        WHERE gr.subject_id = 2  -- Замініть на конкретний ідентифікатор предмета
        GROUP BY g.id, g.name
        ORDER BY group_name;

    """
    result = (
        session.query(
            Group.name.label('group_name'),
            func.round(func.avg(Grade.grade), 2).label('average_grade')
        )
        .join(Student, Group.id == Student.group_id)
        .join(Grade, Student.id == Grade.student_id)
        .filter(Grade.subjects_id == 2)
        .group_by(Group.id, Group.name)
        .order_by(Group.name)
        .all()
    )

    return result

def select_04():
    """
    SELECT ROUND(AVG(grade), 2) AS average_grade
        FROM grades;
    """
    result = (
        session.query(func.round(func.avg(Grade.grade), 2).label('average_grade'))
        .scalar()
    )
    return result

def select_05():
    """
    SELECT s.name AS subject_name
        FROM subjects s
        WHERE s.teacher_id = 1;  -- Замініть на конкретний ідентифікатор викладача

    """
    result = (
        session.query(Subject.name.label('subject_name'))
        .filter(Subject.teacher_id == 1)
        .all()
    )

    return result

def select_06():
    """
    SELECT s.name AS student_name
        FROM students s
        WHERE s.group_id = 2;  -- Замініть на конкретний ідентифікатор групи
    """
    result = (
        session.query(Student.name.label('student_name'))
        .filter(Student.group_id == 2)
        .all()
    )

    return result

def select_07():
    """
    SELECT s.name AS student_name, g.grade, g.grade_date
        FROM students s
        JOIN grades g ON s.id = g.student_id
        WHERE s.group_id = 2 AND g.subject_id = 2;  -- Замініть на конкретні ідентифікатори групи та предмета

    """
    result = (
        session.query(
            Student.name.label('student_name'),
            Grade.grade,
            Grade.grade_date
        )
        .join(Grade, Student.id == Grade.student_id)
        .filter(Student.group_id == 1, Grade.subjects_id == 3)  # Використовуйте необхідні ідентифікатори
        .all()
    )

    return result

def select_08():
    """
    SELECT t.name AS teacher_name, ROUND(AVG(g.grade), 2) AS average_grade
        FROM teachers t
        JOIN subjects s ON t.id = s.teacher_id
        JOIN grades g ON s.id = g.subject_id
        WHERE t.id = 2  -- Замініть на конкретний ідентифікатор викладача
        GROUP BY t.id, t.name;
    """
    result = (
        session.query(
            Teacher.name.label('teacher_name'),
            func.round(func.avg(Grade.grade), 2).label('average_grade')
        )
        .join(Subject, Teacher.id == Subject.teacher_id)
        .join(Grade, Subject.id == Grade.subjects_id)
        .filter(Teacher.id == 2)  # Змініть на потрібний ідентифікатор викладача
        .group_by(Teacher.id, Teacher.name)
        .all()
    )

    return result

def select_09():
    """
    SELECT sub.name AS subject_name
        FROM subjects sub
        JOIN grades gr ON sub.id = gr.subject_id
        WHERE gr.student_id = 25;  -- Замініть на конкретний ідентифікатор студента

    """
    result = (
        session.query(Subject.name.label('subject_name'))
        .join(Grade)
        .filter(Grade.student_id == 25)
        .all()
    )


    return result

def select_10():
    """
SELECT subj.name AS subject_name
FROM subjects subj
JOIN grades g ON subj.id = g.subject_id
JOIN teachers t ON subj.teacher_id = t.id
JOIN students s ON g.student_id = s.id
WHERE t.id = 3  -- Замініть на конкретний ідентифікатор викладача
  AND s.id = 35  -- Замініть на конкретний ідентифікатор студента

    """
    teacher_id = 3  # Змініть на потрібний ідентифікатор викладача
    student_id = 35  # Змініть на потрібний ідентифікатор студента

    result = (
        session.query(Subject.name.label('subject_name'))
        .join(Grade, Subject.id == Grade.subjects_id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .join(Student, Grade.student_id == Student.id)
        .filter(Teacher.id == teacher_id, Student.id == student_id)
        .all()
    )

    return result

def select_11():
    """
SELECT t.name AS teacher_name,
       s.name AS student_name,
       ROUND(AVG(g.grade), 2) AS average_grade
    FROM teachers t
    JOIN subjects subj ON t.id = subj.teacher_id
    JOIN grades g ON subj.id = g.subject_id
    JOIN students s ON g.student_id = s.id
    WHERE t.id = 3  -- Замініть на конкретний ідентифікатор викладача
      AND s.id = 35  -- Замініть на конкретний ідентифікатор студента
    GROUP BY t.name, s.name;

    """
    teacher_id = 3  # Змініть на потрібний ідентифікатор викладача
    student_id = 35  # Змініть на потрібний ідентифікатор студента

    result = (
        session.query(
            Teacher.name.label('teacher_name'),
            Student.name.label('student_name'),
            func.round(func.avg(Grade.grade), 2).label('average_grade')
        )
        .join(Subject, Teacher.id == Subject.teacher_id)
        .join(Grade, Subject.id == Grade.subjects_id)  # Виправлено тут
        .join(Student, Grade.student_id == Student.id)
        .filter(Teacher.id == teacher_id, Student.id == student_id)
        .group_by(Teacher.name, Student.name)
        .all()
    )

    return result
def select_12():
    """
    Отримати останню оцінку для студентів у певній групі та предметі.

    Запити SQL:
    select max(grade_date)
    from grades g
    join students s on s.id = g.student_id
    where g.subject_id = 1 and s.group_id = 2;

    select s.id, s.name, g.grade, g.grade_date
    from grades g
    join students s on g.student_id = s.id
    where g.subject_id = 1 and s.group_id = 2 and g.grade_date = (
        select max(grade_date)
        from grades g
        join students s on s.id = g.student_id
        where g.subject_id = 1 and s.group_id = 2
    );
    """

    # Підзапит для отримання максимальної дати оцінки
    subquery = (
        select(func.max(Grade.grade_date))
        .join(Student, Grade.student_id == Student.id)
        .filter(and_(Grade.subjects_id == 1, Student.group_id == 1))
    ).scalar_subquery()

    subquery = (
        select(func.max(Grade.grade_date))
        .join(Student)
        .filter(and_(Grade.subjects_id == 1, Student.group_id == 1))
    ).scalar_subquery()

    # Основний запит
    result = (
        session.query(Student.id, Student.name, Grade.grade, Grade.grade_date)
        .join(Grade, Student.id == Grade.student_id)
        .filter(and_(
            Grade.subjects_id == 1,  # Використовуйте subjects_id
            Student.group_id == 1,
            Grade.grade_date == subquery  # Використовуйте grade_date
        ))
    ).all()

    return result



if __name__ == '__main__':
    main()
    # print(select_01())
    # print(select_02())
    # print(select_03())
    # print(select_04())
    # print(select_05())
    # print(select_06())
    # print(select_07())
    # print(select_08())
    # print(select_09())
    # print(select_10())
    # print(select_11())
    # print(select_12())
