import pymongo


def main():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        print("Client connected")
        db = client["Student"]
        print("Database Created")
        collection = db["Student_detail"]
        print("Collection Created")


        # Read Operation
        # Insert Single Document
        # collection.insert_one({"name":"Harry", "age":21, "gender":"Male", "marks": [40,50,34]})
        # print("Single Record Inserted")


        # Insert Multiple Record Document
        # data = [
        #     {"name":"Samarth", "age":31, "gender":"Female", "marks": [60,90,94]},
        #     {"name":"Harsh", "age":51, "gender":"Male", "marks": [62,56,94]},
        #     {"name":"Yash", "age":35, "gender":"Female", "marks": [60,40,94]},
        #     {"name":"Kamlesh", "age":37, "gender":"Toxic", "marks": [60,90,94]},
        #     {"name":"Om", "age":60, "gender":"Toxic", "marks": [60,90,94]},
        #     {"name":"Nidhi", "age":60, "gender":"Toxic", "marks": [60,90,94]},
        #     {"name":"Jaivi", "age":60, "gender":"Toxic", "marks": [60,90,94]},
        # ]
        # collection.insert_many(data)



        # Read Operation
        # Read One Record
        print("Finding record of name = Samarth")
        find_by_name = collection.find_one({ "name":"Samarth" })
        print(find_by_name)
        print()

        # Read Multiple Record
        find_all = collection.find({"gender":"Toxic"})
        print("Finding record that have gender = Toxic")
        for document in find_all:
            print(document)
        print()

        # Read only specific column
        print("Finding record that have gender = Toxic but only name and marks columns")
        find_only_specific_col = collection.find({"gender":"Toxic"},{"name":1,"marks":1, "_id":0})
        for document in find_only_specific_col:
            print(document)
        print()

        # Read counts
        print("Finding the number of the records that has been finding")
        print(collection.count_documents({"gender":"Toxic"}))
        print()

        # Read Upto Specific Limit
        print("Finding the specfic number of document that has been finding")
        find_2_document = collection.find({"gender":"Toxic"},{"name": 1, "_id":0}).limit(2)
        for document in find_2_document:
            print(document)
        print()




        # Update Operation
        # Update One Record
        print("Updated One record")
        curr = {"name":"Harry"}
        update = {"$set":{"age": 50}}
        collection.update_one(curr,update)

        # Update Multiple Records
        print("Updated Many Records\n")
        curr = {"age":60}
        update = {"$set":{"age":20}}
        collection.update_many(curr,update)

        # Count modified records
        print("Count Number of records updated\n")
        curr = {"age": 20}
        update = {"$set": {"age": 60}}
        print(collection.update_many(curr,update).modified_count)




        # Delete Records
        # Delete Single Records
        print(f"Delete Single records")
        collection.delete_one({"name":"Harry"})

        # Delete Multiple Records
        data = [
                {"name":"David", "age":99, "gender":"Male", "marks": [60,90,94]},
                {"name":"John", "age":99, "gender":"Male", "marks": [62,56,94]},
                {"name":"Brook", "age":99, "gender":"Female", "marks": [60,40,94]},
        ]
        collection.insert_many(data)
        print(f"Delete Multiple records\n")
        rec = collection.delete_many({"age":99})

        # Counting the number of record deleted
        print(f"Number of records deleted : {rec.deleted_count}\n")




        # method
        # skipping records while printing
        print(f"Skipping the records while printing\n")
        find_all_skip2 = collection.find({"gender": "Toxic"}).skip(2)
        for document in find_all_skip2:
            print(document)

        x=collection.find({"gender": {"$eq": "Toxic"}})
        collection.find({"gender": {"$ne": "Toxic"}})
        collection.find({"age": {"$gt": 51}})
        collection.find({"age": {"$gte": 21}})
        collection.find({"age": {"$lt": 33}})
        collection.find({"age": {"$lte": 51}})
        collection.find({"name": {"$in": ["Harsh", "Samarth"]}})
        collection.find({"name": {"$nin": ["Om", "Alok"]}})

        for i in x:
            print(i)

    except Exception as e:
        print("Failed to connect to database", e)

if __name__ == "__main__":
    main()