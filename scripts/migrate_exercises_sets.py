from db.db import DbSession
from db.models import CustomUserExercise, WorkoutExercise, WorkoutSet


EXERCISE_NAME_TO_CUSTOM_EXERCISE_ID = {
    "Face Pull": "a1d9cc9a-7bf7-402f-954d-5cac0350b02c",
    "Dumbbell Curl": "4584a5c3-d915-4cef-8739-42c5e90eeeb4",
    "Barbell Row": "afb59060-23a3-4cdd-8b6c-6e0ae1b963d9",
    "Leg Press": "97f89a94-38b2-4787-af4d-2f465df66e46",
    "Lunges": "567928df-49cc-4a38-adf8-0b625857df94",
    "Lateral Raise": "e3c769b0-ee19-4512-9397-2dad654a9ddd",
    "Leg Extension": "3eee9777-9776-4a81-88f6-7f5a08b3e8fc",
    "Lat Pulldown": "60938ada-64aa-4b6a-9429-83c6ee91fc67",
    "Deadlift": "28476d67-bc3d-4818-9165-d1c484d33ca1",
    "Dumbbell Row": "098aee44-400e-4396-abe0-59005af67b6a",
    "Cable Row": "9bb8ca9b-8dfe-4a95-b595-f7110cbe4b37",
    "Tricep Dip Machine": "a4427181-c8d6-42e0-815a-7c01bed78547",
    "Lying Leg Curl": "ab3a8e06-0234-470d-8cd9-435650ca3146",
    "Planks": "e836b915-214e-4403-9209-c6379f667aaf",
    "Dumbbell Incline Press": "44a9fed0-7bf3-4482-a723-fbbec64eb3af",
    "Cable Pushdown": "c6e88c04-fdc8-4555-b2a5-77e1b0fa03ff",
    "Dumbbell Reverse Fly": "3ec2be7e-68e0-4e03-bdc4-f254f7c14286",
    "Bench Dips": "a4427181-c8d6-42e0-815a-7c01bed78547",
    "Pull Ups": "30f1f048-8c2e-4b2e-b465-00ee7f5c44cd",
    "Preacher Curl Machine": "30d045fd-f168-4747-a9ed-b9ada3d7d1d3",
    "Tricep Pushdown Machine": "a4427181-c8d6-42e0-815a-7c01bed78547",
    "Backward Walk": "6fc1c83f-1d1a-45a8-bc5e-b55a25a74450",
    "Incline Bench Press": "5ec19ee9-6a1f-4f46-8f16-1ed06bc38f2f",
    "Calf Raises": "1710a4ed-daea-4ade-a163-13ab7239874f",
    "Hip Adductor": "cee82f7c-50b5-4d64-87c8-146294565dcd",
    "Cable Pull Through": "faccdefe-ac04-478b-986c-847970337232",
    "Tricep Extension Machine": "22737612-ee5c-4c20-90d7-5e4e9bdc9c88",
    "Cable Fly": "92c58021-bdca-4092-addd-dfbe49e0397e",
    "Reverse Fly Machine": "c6557d3c-8ce2-4b5c-9150-74105b2aebfd",
}


def map_workout_exercise_to_workout_set(workout_exercise, order):
    return {
        "exercise_id": EXERCISE_NAME_TO_CUSTOM_EXERCISE_ID[
            workout_exercise.exercise_name
        ],
        "workout_id": workout_exercise.workout_id,
        "reps": workout_exercise.reps,
        "order": order,
        "weight": workout_exercise.weight,
        "weight_unit": workout_exercise.weight_unit,
    }


def check_mappable_exercises():
    unmappable_exercises = set()

    print("Workout Exercise Name: Custom User Exercise ID")
    with DbSession() as session:
        for workout_exercise in session.query(WorkoutExercise).all():
            custom_exercise = session.get(
                CustomUserExercise,
                EXERCISE_NAME_TO_CUSTOM_EXERCISE_ID[workout_exercise.exercise_name],
            )

            if custom_exercise:
                # if workout_exercise.exercise_name not in mappable_exercises:
                #     print(f'"{workout_exercise.exercise_name}": "{custom_exercise.id}"')
                #     mappable_exercises.add(workout_exercise.exercise_name)
                pass
            else:
                unmappable_exercises.add(workout_exercise.exercise_name)

        # print(f"Total mappable exercises: {len(mappable_exercises)}")
        # print(f"\nTotal unmappable exercises: {len(unmappable_exercises)}")

        # for exercise in mappable_exercises:
        #     print(f" - {exercise}")

        print("Unmapped exercises:")
        for exercise in unmappable_exercises:
            print(f" - {exercise}")


def migrate_exercises_to_sets():
    with DbSession() as session:
        for workout_exercise in session.query(WorkoutExercise).all():
            for i in range(1, workout_exercise.sets + 1):
                workout_set = map_workout_exercise_to_workout_set(workout_exercise, i)
                session.add(WorkoutSet(**workout_set))
        # commit the changes to the database
        session.commit()


if __name__ == "__main__":
    migrate_exercises_to_sets()
