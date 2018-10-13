class Chip() :
    values = [1, 5, 25, 100];
    def __init__(self, value) :
        if value not in values :
            raise ValueError('${value} is not a valid chip value');
        self.value = value;
        
    def __str__(self) :
        return f'${self.value}';

# NEVER use second and third parameters     
def convert_to_chips(amount, dict={}, i=len(Chip.values)-1) :
    if amount <= 0 :
        while i >= 0 :
            dict[f'${Chip.values[i]} chip'] = 0;
            i -= 1;
        return;
    dict[f'${Chip.values[i]} chip'] = int(amount/Chip.values[i]);
    convert_to_chips(amount%Chip.values[i], dict, i-1);
    return dict;