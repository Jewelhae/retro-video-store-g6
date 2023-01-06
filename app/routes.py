from flask import Blueprint, jsonify, abort, make_response, request 
from app import db 
from app.models.video import Video 
from app.models.customer import Customer
from app.models.rental import Rental

customers_bp = Blueprint("customer_bp", __name__, url_prefix="/customers")
videos_bp = Blueprint("video_bp", __name__, url_prefix="/videos")
rentals_bp = Blueprint("rental_bp", __name__, url_prefix="/rentals")

#--------------------------Helper Functions----------------------------------------------
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except: 
        abort(make_response({"message":f"{cls.__name__} {model_id} is invalid"}, 400)) 

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))    
    return model 

def validate_request_body(request_body): 

    if "name" not in request_body or "phone" not in request_body or "postal_code" not in request_body:
        abort(make_response("Invalid Request", 400))

#validation for Video route
def validate_video_request_body(request_body): 

    if "title" not in request_body or "release_date" not in request_body or "total_inventory" \
        not in request_body:
        abort(make_response("Invalid Request", 400))

#--------------------------- Customer Route Functions -----------------------------------------

@customers_bp.route("/customers", methods=["POST"])
def create_customer():
    request_body = request.get_json()
    #validate_request_body(request_body)

    new_customer = Customer(
        name = request_body["name"],
        postal_code = request_body["postal_code"],
        phone = request_body["phone"],
    )

    db.session.add(new_customer)
    db.session.commit()

    return make_response(jsonify({"id": new_customer.id}, 201))

@customers_bp.route("", methods=["GET"])
def read_all_customers():
    #get a query object for later use
    customer_query = Customer.query

    customers = customer_query.all()
        
    customers_response = [] 

    for customer in customers:
        customers_response.append({
            "id" : customer.id,
            "name": customer.name,
            "postal_code": customer.postal_code,
            "phone": customer.phone,
            "register_at": customer.register_at, 
            #"videos_checked_out_count":customer.videos_checked_out_count
        })
    #return jsonify(customers_response)
    
    # for customer in customers: 
    #     customer_response.append(customer.to_dict())    #use to_dict function to make code more readable

    return make_response(jsonify(customers_response), 200)

@customers_bp.route("/<customer_id>", methods=["GET"])
def read_one_customer_by_id(customer_id):
    customer = validate_model(Customer, customer_id)

    return (customer.to_dict(),200)

@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer_by_id(customer_id):
    customer = validate_model(Customer, customer_id)

    request_body = request.get_json() 
    validate_request_body(request_body)

    customer.name = request_body["name"]
    customer.postal_code = request_body["postal_code"]
    customer.phone = request_body["phone"]

    db.session.commit() 

    return make_response(jsonify(f"Customer: {customer_id} has been updated successfully."), 200) 

@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer_by_id(customer_id): 
    customer = validate_model(Customer, customer_id)  

    db.session.delete(customer)
    db.session.commit()

    return make_response(jsonify(f"Customer: {customer_id} has been deleted successfully."), 200) 

######################
######################
#--------Video--------
######################
#--------------------------- Video Route Functions -----------------------------------------

@videos_bp.route("", methods=["POST"])
def create_one_video():
    request_body = request.get_json()
    validate_video_request_body(request_body)

    new_video = Video.from_dict(request_body)

    print(new_video.title)
    db.session.add(new_video)
    db.session.commit()

    return new_video.to_dict(), 201

@videos_bp.route("", methods=["GET"])
def read_all_videos():
    #get a query object for later use
    video_query = Video.query

    videos = video_query.all()
        
    video_response = [] 
    for video in videos: 
        video_response.append(video.to_dict())    #use to_dict function to make code more readable
    #print(video_response)
    return jsonify(video_response)

@videos_bp.route("/<video_id>", methods=["GET"])
def read_one_video_by_id(video_id):
    video = validate_model(Video, video_id)

    return (video.to_dict(),200)

@videos_bp.route("/<video_id>", methods=["PUT"])
def update_video_by_id(video_id):
    video = validate_model(Video, video_id)

    request_body = request.get_json() 
    validate_video_request_body(request_body)

    video.title = request_body["title"]
    video.release_date = request_body["release_date"]
    video.total_inventory = request_body["total_inventory"]

    db.session.commit() 

    return make_response(jsonify(f"Video: {video_id} has been updated successfully."), 200) 

@videos_bp.route("/<video_id>", methods=["DELETE"])
def delete_video_by_id(video_id): 
    video = validate_model(Video, video_id)  

    db.session.delete(video)
    db.session.commit()

    return make_response(jsonify(f"Video: {video_id} has been deleted successfully."), 200) 

#--------------------------- Rentals Route Functions -----------------------------------------
@rentals_bp.route("", methods=["GET"])
def create_rental():
    request_body = request.get_json()
    new_rental = Rental(
        name=request_body["name"],
    )
    db.session.add(new_rental)
    db.session.commit()

    return make_response(jsonify(f"Rental {new_rental}"))