"""Dựng video bài giảng từ kịch bản YAML: hai giọng đọc miễn phí, slide có phụ đề, mục lục chương.

Kịch bản nằm cạnh sách: books/<sách>/lessons/<id>.yaml. Kết quả: <id>.mp4 cùng thư mục và một mục
trong books/<sách>/lessons/lessons.json để tab Sách gắn video vào đúng hoạt động của unit.
Không đụng book.json / plan.json (việc của agent nhập sách).
"""
