# from pymongo import MongoClient
# from fastapi import FastAPI, HTTPException, status
# from pydantic import BaseModel, StrictStr, StrictInt, StrictFloat, Field
# from typing import List
#
# app = FastAPI()
#
# def connect_mongodb():
#     """
#     Connect to MongoDB
#     Returns - collection
#     -------
#     """
#
#     try:
#         client = MongoClient("mongodb://localhost:27017/")
#         print("Connected to MongoDB")
#
#         database = client.get_database("Tutorial_1")
#         collection = database["Test2"]
#         return collection
#
#     except ConnectionError as error:
#         print("Connection Error - ", error)
#
#     except Exception as error:
#         print(error)
#
# class Student(BaseModel):
#     name: StrictStr
#     age: StrictInt = Field(gt = 0, lt = 25)
#     marks: List[StrictFloat] = List[Field(gt = 0, lt = 25)]
#
# @app.post("/add_students", status_code = status.HTTP_201_CREATED)
# def add_students(request: Student):
#     """
#     Add students
#     Parameters
#     ----------
#     request : Student --> BaseModel
#
#     Returns - Added message
#     -------
#
#     """
#
#     db = connect_mongodb()
#
#     total_students = [i for i in db.find()]
#     _id = len(total_students) + 1
#
#     if db.count_documents({"name": request.name}) > 0:
#         raise HTTPException(status_code = 400, detail = "Student already exists")
#
#     db.insert_one(
#         {
#             "_id": _id,
#             "name": request.name,
#             "age": request.age,
#             "marks": request.marks,
#         }
#     )
#     return {"message": f"ID {_id} - Student( {request.name} ) Added Successfully"}
#
# @app.get("/students", status_code = status.HTTP_200_OK)
# def get_students():
#     """
#     Get students
#     Parameters
#     ----------
#     request - Student --> BaseModel
#
#     Returns - all student details
#     -------
#
#     """
#
#     db = connect_mongodb()
#
#     total_students = [i for i in db.find()]
#     return total_students
#
# @app.get("/students/{_id}", status_code = status.HTTP_200_OK)
# def get_students_by_id(_id: int):
#     """
#     Get student details by ID
#     Parameters
#     ----------
#     _id - Student ID
#
#     Returns - student detail
#     -------
#     """
#
#     db = connect_mongodb()
#
#     student = db.find_one({"_id": _id})
#     return student
from typing import List,Optional
from fastapi import FastAPI,HTTPException, status
import pymongo
from pydantic import BaseModel, StrictStr, StrictInt, Field, StrictFloat
from pymongo.errors import ConnectionFailure
from sqlalchemy.sql.annotation import Annotated

app = FastAPI()

class Student(BaseModel):
    name: StrictStr = Field(..., max_length=50)
    age: StrictInt = Field(...)
    marks: List[StrictFloat] = Field(...,max_length=3)


class Patchstudent(BaseModel):
    name: Optional[StrictStr] = Field(None, max_length=50)
    age: Optional[StrictInt] = Field(None, le=99)
    marks: Optional[List[StrictFloat]] = Field(None, max_length=3)


def connect_db():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017")
        print("Client Created")

        db = client["Student"]
        print("Database Connected")

        collection = db["Student_data"]
        print("Collection Created")
        return collection

    except ConnectionError as e:
        print(f"Connection Error : {e}")
    except pymongo.errors.ConnectionFailure as e:
        print(f"Connection Failed : {e}")
    except Exception as e:
        print(f"Unknown error Occured: {e}")



@app.get("/get_all", status_code=status.HTTP_200_OK, tags=["Get All Data"])
def get_all():
    db = connect_db()

    res = [i for i in db.find()]
    if res:
        return res
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Record Found")



@app.get("/get_one/{student_id}", status_code=status.HTTP_200_OK, tags=["Get One Data"])
def get_one(student_id:int):
    db = connect_db()

    res = db.find_one({"_id": student_id})
    if res:
        return res
    else:
        return f"Student Id : {student_id} not found"


@app.post("/insert_one", status_code=status.HTTP_201_CREATED, tags=["Insert One Data"])
def insert_one(data: Student):
    db = connect_db()
    student_id = db.count_documents({}) + 1

    db.insert_one({
        "_id":student_id,
        "name": data.name,
        "age": data.age,
        "marks": data.marks,
    })

    return f"Id : {student_id} with student name : {data.name} inserted successfully"


@app.put("/put_student/{student_id}", status_code=status.HTTP_200_OK, tags=["Put Student Data"])
def put_student(student_id:int,data: Student):
    db = connect_db()

    update_data = data.model_dump()
    res = db.find_one({"_id": student_id})
    if res:
        db.update_one({"_id": student_id}, {"$set": update_data})
        return f"Student ID : {student_id} updated successfully"
    else:
        return f"Student Id : {student_id} not found"



@app.patch("/patch_student/{student_id}", status_code=status.HTTP_200_OK, tags=["Patch Student Data"])
def patch_student(student_id:int, data: Patchstudent):

    db = connect_db()
    update_data = data.model_dump()
    res = db.find_one({"_id": student_id})
    if res:
        db.update_one({"_id": student_id}, {"$set": update_data})
        return f"Student ID : {student_id} updated successfully"
    else:
        return f"Student Id : {student_id} not found"


# @app.patch("/student/{id_}",status_code=status.HTTP_200_OK,tags=["Update"])
# def patch_student(req_data: Student,id_:int):
#     """
#     :param req_data: Student
#     :param id_: int
#     :return: Success message along with id of the student
#     """
#     collection = connect_db()
#     db_rec = collection.find_one({"id":id})
#     if not db_rec:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found")
#
#     collection.update_one({"id": id},{"$set":{"name":req_data.name if not req_data.name !="string" else db_rec["name"],
#                                                 "age":req_data.age if req_data.age != 1 else db_rec["age"],
#                                                 "gender":req_data.gender if req_data.gender != "string" else db_rec["gender"],
#                                                 "marks":req_data.marks if req_data.marks != [0] else db_rec["marks"]
#                                                 }
#                                         }
#                           )
#     return f"Student {id_} updated successfully"

# Delete
@app.delete("/student/{id_}",status_code=status.HTTP_202_ACCEPTED,tags=["Delete"])
def delete_student(id_:int):
    """
    :param id_: int
    :return: Success message along with id of the student
    """
    collection = connect_db()
    db_rec = collection.find_one({"id":id})
    if not db_rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found")
    collection.delete_one({"id": id})
    return f"Student {id_} deleted successfully"


