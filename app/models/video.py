from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    total_inventory = db.Column(db.Integer, default=0)

    rentals = db.relationship('Rental', back_populates='video')

    def to_dict(self):
        video_as_dict = {}
        video_as_dict["id"] = self.id
        video_as_dict["title"] = self.title
        video_as_dict["release_date"] = self.release_date
        video_as_dict["total_inventory"] = self.total_inventory     
        return video_as_dict

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }

    def get_available_video_inventory(self):
        num_of_rentals = 0
        for rental in self.rentals:
            if rental.is_checked_out:
                num_of_rentals += 1
        return self.total_inventory - num_of_rentals

    @classmethod
    def get_id(cls, id):
        return Video.query.get(id)

    @classmethod
    def from_dict(cls, video_data):
        new_video = Video(title = video_data["title"],
                        release_date=video_data["release_date"],
                        total_inventory = video_data['total_inventory'])
        return new_video
