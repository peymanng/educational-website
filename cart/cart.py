from django.conf import settings
from courses.models import Course


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    # add to cart
    def add(self, course):
        course_id = str(course.id)
        if course_id not in self.cart:
            if course.discount:
                self.cart[course_id] = {'price': (int(course.price) - int((course.price * course.discount)/100)) }
            else:
                self.cart[course_id] = {'price': course.price}
        self.save()

    def save(self):
        self.session.modified = True

    # remove from cart
    def remove(self, course):
        course_id = str(course.id)
        if course_id in self.cart:
            del self.cart[course_id]
            self.save()

    def __iter__(self):
        course_ids = self.cart.keys()
        courses = Course.objects.filter(id__in=course_ids)

        cart = self.cart.copy()
        for course in courses:
            cart[str(course.id)]['course'] = course

        for item in cart.values():
            item['total_price'] = item['price']
            yield item

    def __len__(self):
        return len(self.cart.values())

    @property
    def get_course_ids(self):
        courses_ids = []
        for key in self.cart.keys():
            courses_ids.append(int(key))
        return courses_ids

    def get_total_price(self):
        return sum(item['price'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def is_empty(self):
        return self.get_course_ids == []