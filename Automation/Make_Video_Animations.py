
import math

#this is where all of the animations will go

# slowly come in, and overshoot before coming back to the final size
def ease_out_back(t, duration, overshoot=1.7):
    
    # need to get the percent it is through the animation [0,1] 
    x = t / duration
    x = min(1, x) # make sure it is not greater than 1
    
    c2 = overshoot + 1
    
    return 1 + c2 * math.pow(x - 1, 3) + overshoot * math.pow(x - 1, 2)


# overshoot a bit before going all the way out
def ease_in_back(t, duration, overshoot=1.7):
    
    # need to get the percent it is through the animation [0,1] 
    x = t / duration
    x = min(1, x) # make sure it is not greater than 1
    
    c2 = overshoot + 1
    
    return c2 * x * x * x - overshoot * x * x




# slide the text in from the right and overshoot. then slide left overshoor on the way out right
def slide_in_slide_out(t, in_time, out_time, duration, pos_x, overshoot, right_movement):
    """
    t: current time
    in_time: how long i allow the animation to take in
    out_time: how long i allow the animation to take out
    duration: the total duration of the clip
    pos_x: the starting/ending x position of the text
    overshoot: the amount to overshoot to the left before coming back
    right_movement: the amount to move to the right so the end position
    """
    
    # start animating out
    if t > duration - out_time:
        # calculate the percent of the way through the animation
        
        ease_value = ease_in_back((t - (duration - out_time)), out_time, overshoot)
        
        # move the text to the right
        new_x = pos_x + (ease_value * right_movement)
        
        #print(f"func({t}, {start_out_t}, {duration}, {pos_x}) = {ease_value}")
        return new_x
    
    elif t < in_time: # start animating in
        # calculate the percent of the way through the animation
        ease_value = ease_in_back(in_time-t, in_time, overshoot)
        
        # move the text to the right
        new_x = pos_x + (ease_value * right_movement)
        
        return new_x
    
    
    else: # its not sliding in or out
        return pos_x
        
    
    
    
# pop the text in and also out at the end
def pop_in_pop_out_size(t, in_time, out_time, clip_duration, max_width, max_height, overshoot=2):
    
    # start animating out
    if t > clip_duration - out_time:
        # so if it is greater than the clip duration, then just return the max width and height
        easy_out_back_value = ease_out_back(clip_duration - t, out_time, overshoot)
        
        new_width = max_width * easy_out_back_value
        new_height = max_height * easy_out_back_value
        
        # make sure it is greater than 0
        new_width = max(new_width, 1)
        new_height = max(new_height, 1)
        
        
        return (new_width, new_height)
        
    elif t < in_time: # start animating in
        # so if it is greater than the clip duration, then just return the max width and height
        easy_out_back_value = ease_out_back(t, in_time, overshoot)
        
        new_width = max_width * easy_out_back_value
        new_height = max_height * easy_out_back_value
        
        # make sure it is greater than 0
        new_width = max(new_width, 1)
        new_height = max(new_height, 1)
        
        #print(f"t({round(t, 2)}): ({round(new_width, 2)}, {round(new_height, 2)})")
        return (new_width, new_height)
        
    else: # its not sliding in or out
        #print(f"t({round(t, 2)}): ({round(max_width, 2)}, {round(max_height, 2)})")
        return (max_width, max_height)
    
    
# POP IN (Used for Quick and Thanks)
# this goes along with the new size to keep the text centered as it gets bigger over time
def pop_in_pop_out_position(t, in_time, out_time, clip_duration, max_width, max_height, screen_size, max_x, max_y, overshoot=2):
    if t > clip_duration:
        return (max_x, max_y)
    
    # Calculate the current size based on the zoom effect
    current_size_factor = pop_in_pop_out_size(t, in_time, out_time, clip_duration, max_width, max_height, overshoot)  # Assuming new_size returns a factor, not pixel dimensions

    new_x = (screen_size[0]/2 + max_x) - current_size_factor[0] / 2
    new_y = (screen_size[1]/2 + max_y) - current_size_factor[1] / 2
    return (new_x, new_y)

    






# gpt ease in pop in animation Used for Quick and Thanks
def pop_in_size(t, clip_duration, max_width, max_height, overshoot):
    
    # so if it is greater than the clip duration, then just return the max width and height

    easy_out_back_value = ease_out_back(t, clip_duration, overshoot)
    
    new_width = max_width * easy_out_back_value
    new_height = max_height * easy_out_back_value
    
    # make sure it is greater than 0
    new_width = max(new_width, 1)
    new_height = max(new_height, 1)
    
    return (new_width, new_height)








# POP IN (Used for Quick and Thanks)
# this goes along with the new size to keep the text centered as it gets bigger over time
def pop_in_position(t, max_width, max_height, screen_size, max_x, max_y, duration, overshoot):
    if t > duration:
        return (max_x, max_y)
    
    # Calculate the current size based on the zoom effect
    current_size_factor = pop_in_size(t, max_width, max_height, duration, overshoot)  # Assuming new_size returns a factor, not pixel dimensions

    new_x = (screen_size[0]/2 + max_x) - current_size_factor[0] / 2
    new_y = (screen_size[1]/2 + max_y) - current_size_factor[1] / 2
    return (new_x, new_y)



    