from functools import partial
from tkinter import *
import tkinter.messagebox as mb
from Data import Data
from ClusterAnalysis import ClusterAnalysis
from Point import Point

root = Tk()
root.title('Кластерный анализ')
root.geometry('700x500')
root.iconbitmap(r'c:\users\peg\PycharmProjects\lab_09\ClusterAnalysis.ico')


def choice_color():
    colors = ['red', 'green', 'yellow', 'purple', 'orange', 'blue', 'khaki', 'brown', 'tomato', 'gold', 'pink',
              'darkblue', 'indigo', 'seagreen', 'olive', 'dimgray', 'lawngreen']
    color = colors[root.counter]
    root.counter += 1
    if root.counter == len(colors):
        root.counter = 0
    return color


def button_points(canvas, data):
    canvas.bind('<Button-1>', partial(paint, canvas=canvas, figure='oval', data=data))


def button_new_cluster(canvas, data):
    canvas.bind('<Button-1>', partial(paint, canvas=canvas, figure='square', data=data))


def button_calculation(canvas, data):
    if data.metric is None and not data.global_points and not data.global_centroids:
        message = 'Исходные занчения не заданы'
        mb.showerror('Ошибка', message)
    elif data.metric is None:
        message = 'Метрика не задана'
        mb.showerror('Ошибка', message)
    elif not data.global_points:
        message = 'Точки не заданы'
        mb.showerror('Ошибка', message)
    elif not data.global_centroids:
        message = 'Центры класстеров не заданы'
        mb.showerror('Ошибка', message)
    else:
        cluster_analysis = ClusterAnalysis(data.global_centroids, data.global_points, data.metric)
        print('Starting points:')
        data.print_points()
        print('Starting centers of clusters:')
        data.print_centroids()
        print()
        canvas.bind('<Button-1>', partial(step, canvas=canvas, cluster_analysis=cluster_analysis))


def step(event, canvas, cluster_analysis):
    cluster_analysis.k_means()
    canvas.delete('all')
    points = cluster_analysis.points
    centroids = cluster_analysis.centroids
    for point in points:
        x1, y1 = (point.x - 6), (point.y - 6)
        x2, y2 = (point.x + 6), (point.y + 6)
        canvas.create_oval(x1, y1, x2, y2, fill=point.color)
    for centroid in centroids:
        x1, y1 = (centroid.x - 8), (centroid.y - 8)
        x2, y2 = (centroid.x + 8), (centroid.y + 8)
        canvas.create_rectangle(x1, y1, x2, y2, fill=centroid.color, outline=centroid.color)


def choice_metric(metric, data):
    if metric == 'Euclidean':
        data.metric = 'Euclidean'
    else:
        data.metric = 'Chebyshev'


def button_return(canvas, data):
    message = 'Вы уверены, что хотите вернуться на начальный этап?'
    if mb.askyesno(message=message):
        data.delete_metric()
        canvas.delete('all')
        points = data.global_points
        x = data.coordinate_x
        y = data.coordinate_y
        for point in points:
            point.color = 'black'
            x1, y1 = (point.x - 6), (point.y - 6)
            x2, y2 = (point.x + 6), (point.y + 6)
            canvas.create_oval(x1, y1, x2, y2, fill=point.color)
        for index in range(len(data.global_centroids)):
            centroid = data.global_centroids[index]
            centroid.x = x[index]
            centroid.y = y[index]
            x1, y1 = (x[index] - 8), (y[index] - 8)
            x2, y2 = (x[index] + 8), (y[index] + 8)
            canvas.create_rectangle(x1, y1, x2, y2, fill=centroid.color, outline=centroid.color)
        canvas.unbind('<Button-1>')


def button_clear(canvas, data):
    message = 'Вы уверены, что хотите очистить поле?'
    if mb.askyesno(message=message):
        data.delete_centroids()
        data.delete_points()
        data.delete_metric()
        data.delete_coordinate()
        data.delete_number()
        canvas.delete('all')
        canvas.unbind('<Button-1>')


def paint(event, canvas, figure, data):
    if figure == 'oval':
        x1, y1 = (event.x - 6), (event.y - 6)
        x2, y2 = (event.x + 6), (event.y + 6)
        color = 'black'
        data.add_point(Point(event.x, event.y, color, data.number_point))
        data.number_point += 1
        canvas.create_oval(x1, y1, x2, y2, fill=color)
    else:
        x1, y1 = (event.x - 8), (event.y - 8)
        x2, y2 = (event.x + 8), (event.y + 8)
        color = choice_color()
        data.add_centroids(Point(event.x, event.y, color, data.number_centroid))
        data.number_centroid += 1
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)


def main():
    data = Data()
    main_menu = Menu(root)
    root.config(menu=main_menu)
    root.counter = 0
    canvas = Canvas(root, width=700, height=500)
    canvas.pack(expand=YES, fill=BOTH)
    metric_menu = Menu(main_menu, tearoff=0)
    metric_menu.add_command(label='Евклидова', command=partial(choice_metric, metric='Euclidean', data=data))
    metric_menu.add_command(label='Чебышёва', command=partial(choice_metric, metric='Chebyshev', data=data))
    main_menu.add_command(label='Точки', command=partial(button_points, canvas=canvas, data=data))
    main_menu.add_command(label='Новый кластер', command=partial(button_new_cluster, canvas=canvas, data=data))
    main_menu.add_command(label='Расчет', command=partial(button_calculation, canvas=canvas, data=data))
    main_menu.add_cascade(label='Метрика', menu=metric_menu)
    main_menu.add_command(label='Восстановить', command=partial(button_return, canvas=canvas, data=data))
    main_menu.add_command(label='Очистка', command=partial(button_clear, canvas=canvas, data=data))
    root.mainloop()


if __name__ == '__main__':
    main()
