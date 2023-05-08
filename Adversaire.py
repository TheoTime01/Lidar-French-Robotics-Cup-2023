import math

class Adversary:
    def __init__(self, data):
        print ("Inititalisation ")
        self.data = data

    def calculate_opposite_side(self):
        """ Calculate the opposite side of the angle with the Al Kashi theory "
            Args:
                D: the list of distances and angles D={angle:distance}
            Returns:
                results: the opposite side for each consecutive angle
        """
        results = {}
        for angle in range(0,359):
            opposite = 0
            next_angle = angle +1
            angle_rad= math.radians(angle)
            angle_rad_next= math.radians(next_angle)
            opposite = (self.data[angle])**2 + (self.data[next_angle])**2 -2*self.data[angle]* self.data[next_angle]*math.cos(angle_rad_next-angle_rad)
            opposite = math.sqrt(opposite)
            results[angle] = opposite

        return results

    def is_detected(self):
        """ Return True if the opposite side is greater than 190mm between the angles 20 degrees and 160 degrees
            Args:
                D: the list of distances and angles D={angle:distance}
            Returns:
                True if the opposite side is greater than 190mm between the angles 90 degrees and 270 degrees
                False otherwise
        """
        data2 = self.calculate_opposite_side()
        opp=0
        a=0
        for angle in self.data:
            if 90<angle<270 :
                if 40<self.data[angle]<60:
                    if angle-a < 3:
                        opp = opp + data2[angle]
                        a=angle
                    else:
                        break
            
        if opp>=100:
            print("enemy spotted")
            return True
        else:
            return False
