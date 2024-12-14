from src.schema.request_format import LabelsValidator

test = LabelsValidator()
test.labels = "jdjadj"
print(test.model_dump())
