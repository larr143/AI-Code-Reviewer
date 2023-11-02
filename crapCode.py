def calculate_area_of_rectangle(length, width):
    area= length*width
    return area

def print_rectangle_properties(length,width):
    print("Length of rectangle: ",length)
    print("Width of rectangle: ", width)
    print("Area: ", calculate_area_of_rectangle(length,width))

length_of_rectangle=10
width_of_rectangle=5

print_rectangle_properties(length_of_rectangle,width_of_rectangle)