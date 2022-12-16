import matplotlib.pyplot as plt
def get_a_chart(vals):
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot()
    labels = ['Еда', 'Транспорт', 'Связь', 'Досуг', 'Покупки', 'Здоровье', 'Другое']
    exp = [0, 0, 0, 0, 0, 0, 0]
    i=0
    for _ in range(len(vals)):
        try:
            if vals[i]==0:
                vals.pop(i)
                labels.pop(i)
                exp.pop(i)
                i-=1
        except:
            pass
        i += 1
    if len(vals)==0:
        return False


    ax.pie(vals, labels=labels, autopct='%2.f', wedgeprops=dict(width=1))
    plt.savefig('temp_chart.png')
    return True
