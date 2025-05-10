FROM python:3.13.3-bookworm

COPY requirements.txt .

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

ENV senderemail="warszawski.krystian98@gmail.com"
ENV receiveremail="krystian.warszawski98@gmail.com"
ENV emailerpassword="bbim fuey vwqw uxup"

COPY src .

CMD bash