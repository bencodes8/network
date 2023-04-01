from django.core.paginator import Paginator

objects = ['a', 'b', 'c', 'd']
p = Paginator(objects, 2)

print(p.count)
print(p.num_pages)
print(p.page_range)
print(p.page(1))

page1 = p.page(1)
print(page1.object_list)