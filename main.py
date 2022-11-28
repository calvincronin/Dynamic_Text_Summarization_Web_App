from flask import Flask, render_template, Response, request, redirect, url_for
import transformers

app = Flask(__name__)

fulltext = """Walking back to camp through the swamp, Sam wondered whether to tell his
father what he had seen.
“I know one thing,” he said to himself. “I’m going back to that little pond
again tomorrow. And I’d like to go alone. If I tell my father what I saw today, he
will want to go with me. I’m not sure that’s a very good idea.”
Sam was eleven. His last name was Beaver. He was strong for his age and
had black hair and dark eyes like an Indian. Sam walked like an Indian, too,
putting one foot straight in front of the other and making very little noise. The
swamp through which he was traveling was a wild place—there was no trail, and
it was boggy underfoot, which made walking difficult. Every four or five
minutes Sam took his compass out of his pocket and checked his course to make
sure he was headed in a westerly direction. Canada is a big place. Much of it is
wilderness. To get lost in the woods and swamps of western Canada would be a
serious matter.
As he trudged on, the boy’s mind was full of the wonder of what he had
seen. Not many people in the world have seen the nest of a Trumpeter Swan.
Sam had found one on the lonely pond on this day in spring. He had seen the two
great white birds with their long white necks and black bills. Nothing he had
ever seen before in all his life had made him feel quite the way he felt, on that
wild little pond, in the presence of those two enormous swans. They were so
much bigger than any bird he had ever seen before. The nest was big, too—a
mound of sticks and grasses. The female was sitting on eggs; the male glided
slowly back and forth, guarding her.
When Sam reached camp, tired and hungry, he found his father frying a
couple of fish for lunch.
“Where have you been?” asked Mr. Beaver.
“Exploring,” replied Sam. “I walked over to a pond about a mile and a half
from here. It’s the one we see from the air as we’re coming in. It isn’t much of a
place—nowhere near as big as this lake we’re on.”
“Did you see anything over there?” asked his father.
“Well,” said Sam, “it’s a swampy pond with a lot of reeds and cattails. I
don’t think it would be any good for fishing. And it’s hard to get to—you have
to cross a swamp.”
“See anything?” repeated Mr. Beaver.
“I saw a muskrat,” said Sam, “and a few Red-winged Blackbirds.”
Mr. Beaver looked up from the wood stove, where the fish were sizzling in a
pan.
“Sam,” he said, “I know you like to go exploring. But don’t forget—these
woods and marshes are not like the country around home in Montana. If you
ever go over to that pond again, be careful you don’t get lost. I don’t like you
crossing swamps. They’re treacherous. You could step into a soggy place and
get bogged down, and there wouldn’t be anybody to pull you out.”
“I’ll be careful,” said Sam. He knew perfectly well he would be going back
to the pond where the swans were. And he had no intention of getting lost in the
woods. He felt relieved that he had not told his father about seeing the swans,
but he felt queer about it, too. Sam was not a sly boy, but he was odd in one
respect: he liked to keep things to himself. And he liked being alone, particularly
when he was in the woods. He enjoyed the life on his father’s cattle ranch in the
Sweet Grass country in Montana. He loved his mother. He loved Duke, his cow
pony. He loved riding the range. He loved watching guests who came to board at
the Beavers’ ranch every summer.
But the thing he enjoyed most in life was these camping trips in Canada with
his father. Mrs. Beaver didn’t care for the woods, so she seldom went along—it
was usually just Sam and Mr. Beaver. They would motor to the border and cross
into Canada. There Mr. Beaver would hire a bush pilot to fly them to the lake
where his camp was, for a few days of fishing and loafing and exploring. Mr.
Beaver did most of the fishing and loafing. Sam did the exploring. And then the
pilot would return to take them out. His name was Shorty. They would hear the
sound of his motor and run out and wave and watch him glide down onto the
lake and taxi his plane in to the dock. These were the pleasantest days of Sam’s
life, these days in the woods, far, far from everywhere—no automobiles, no
roads, no people, no noise, no school, no homework, no problems, except the
problem of getting lost. And, of course, the problem of what to be when he grew
up. Every boy has that problem.
After supper that evening, Sam and his father sat for a while on the porch.
Sam was reading a bird book.
“Pop,” said Sam, “do you think we’ll be coming back to camp again about a
month from now—I mean, in about thirty-five days or something like that?”
“I guess so,” replied Mr. Beaver. “I certainly hope so. But why thirty-five
days? What’s so special about thirty-five days?”
“Oh, nothing,” said Sam. “I just thought it might be very nice around here in
thirty-five days.”
“That’s the craziest thing I ever heard of,” said Mr. Beaver. “It’s nice here
all the time.”
Sam went indoors. He knew a lot about birds, and he knew it would take a
swan about thirty-five days to hatch her eggs. He hoped he could be at the pond
to see the young ones when they came out of the eggs.
Sam kept a diary—a daybook about his life. It was just a cheap notebook that
was always by his bed. Every night, before he turned in, he would write in the
book. He wrote about things he had done, things he had seen, and thoughts he
had had. Sometimes he drew a picture. He always ended by asking himself a
question so he would have something to think about while falling asleep. On the
day he found the swan’s nest, this is what Sam wrote in his diary:
I saw a pair of trumpeter swans today on a small pond east of camp.
The female has a nest with eggs in it. I saw three, but I’m going to put
four in the picture—I think she was laying another one. This is the
greatest discovery I ever made in my entire life. I did not tell Pop. My
bird book says baby swans are called cygnets. I am going back tomorrow
to visit the great swans again. I heard a fox bark today. Why does a fox
bark? Is it because he is mad, or worried, or hungry, or because he is
sending a message to another fox? Why does a fox bark?
Sam closed his notebook, undressed, crawled into his bunk, and lay there
with his eyes closed, wondering why a fox barks. In a few minutes he was
asleep."""
fulltext = fulltext.replace('\n',' ')

quoting = False
idxs = []
ignoreperiod = ['Mr', 'Ms', 'Mrs', 'Dr', 'Sr']
for count, char in enumerate(fulltext):
    if count > 0:
        prevchar = fulltext[count-1]
        if prevchar == '“':
            quoting = True
        elif prevchar == '”':
            quoting = False
        if char == '”' and prevchar == '.':
            idxs.append(count)
        elif char == '.':
            ppchar = fulltext[count-2]
            pppchar = fulltext[count-3]
            beforeperiod = (pppchar+ppchar+prevchar).replace(' ','')
            if beforeperiod not in ignoreperiod:
                if not quoting:
                    idxs.append(count)

sentances = []
for count, idx in enumerate(idxs):
    if count < 1:
        start = 0
    else:
        start = idxs[count - 1] + 2
    stop = idx + 1
    sent = fulltext[start:stop]
    sentances.append(sent)

sentcount = len(sentances)
binsize = int(sentcount/5)

i = 0
tempbin = []
bins = []
for sent in sentances:
    i += 1
    if i == binsize:
        bin = ' '.join(tempbin)
        bins.append(bin)
        tempbin = []
        i = 0
    tempbin.append(sent)

nlp = transformers.pipeline("summarization", model='sshleifer/distilbart-cnn-12-6', revision='a4f8f3e')    

master_dic = {}
for count, parag in enumerate(bins):
    count = count + 1
    master_dic.update({count:{}})
    ssplit = parag.split(' ')
    totallen = len(ssplit)
    for i in range(1,5):
        if i == 1:
            master_dic[count].update({i : parag})
        else:
            ml_i = int(totallen/i)
            sum_i = nlp(parag, min_length = ml_i-20, max_length = ml_i)[0]['summary_text']
            master_dic[count].update({i : sum_i})

data_i = []

for parnum, sumdic in master_dic.items():
    tempdic = {
        'parnum' : parnum,
        'sumlevel' : 1,
        'content' : sumdic[1]
    }
    data_i.append(tempdic)

@app.route("/")
def hello():
    return render_template('homep.html', data_i = data_i)

@app.route("/p1up/", methods=['POST'])
def p1up():
    if data_i[0]['sumlevel'] < 4:
        newlevel = data_i[0]['sumlevel'] + 1
        newcontent = master_dic[1][newlevel]
        data_i[0]['sumlevel'] = newlevel
        data_i[0]['content'] = newcontent
    return render_template('homep.html', data_i = data_i)

@app.route("/p2up/", methods=['POST'])
def p2up():
    if data_i[1]['sumlevel'] < 4:
        newlevel = data_i[1]['sumlevel'] + 1
        newcontent = master_dic[2][newlevel]
        data_i[1]['sumlevel'] = newlevel
        data_i[1]['content'] = newcontent
    return render_template('homep.html', data_i = data_i)

@app.route("/p3up/", methods=['POST'])
def p3up():
    if data_i[2]['sumlevel'] < 4:
        newlevel = data_i[2]['sumlevel'] + 1
        newcontent = master_dic[3][newlevel]
        data_i[2]['sumlevel'] = newlevel
        data_i[2]['content'] = newcontent
    return render_template('homep.html', data_i = data_i)

@app.route("/p4up/", methods=['POST'])
def p4up():
    if data_i[3]['sumlevel'] < 4:
        newlevel = data_i[3]['sumlevel'] + 1
        newcontent = master_dic[4][newlevel]
        data_i[3]['sumlevel'] = newlevel
        data_i[3]['content'] = newcontent
    return render_template('homep.html', data_i = data_i)

@app.route("/p5up/", methods=['POST'])
def p5up():
    if data_i[4]['sumlevel'] < 4:
        newlevel = data_i[4]['sumlevel'] + 1
        newcontent = master_dic[5][newlevel]
        data_i[4]['sumlevel'] = newlevel
        data_i[4]['content'] = newcontent
    return render_template('homep.html', data_i = data_i)


@app.route("/p1down/", methods=['POST'])
def p1down():
    if data_i[0]['sumlevel'] > 1:
        newlevel = data_i[0]['sumlevel'] - 1
        newcontent = master_dic[1][newlevel]
        data_i[0]['sumlevel'] = newlevel
        data_i[0]['content'] = newcontent
    return render_template('homep.html', data_i = data_i)

@app.route("/p2down/", methods=['POST'])
def p2down():
    if data_i[1]['sumlevel'] > 1:
        newlevel = data_i[1]['sumlevel'] - 1
        newcontent = master_dic[2][newlevel]
        data_i[1]['sumlevel'] = newlevel
        data_i[1]['content'] = newcontent
    return render_template('homep.html', data_i = data_i)

@app.route("/p3down/", methods=['POST'])
def p3down():
    if data_i[2]['sumlevel'] > 1:
        newlevel = data_i[2]['sumlevel'] - 1
        newcontent = master_dic[3][newlevel]
        data_i[2]['sumlevel'] = newlevel
        data_i[2]['content'] = newcontent
    return render_template('homep.html', data_i = data_i)

@app.route("/p4down/", methods=['POST'])
def p4down():
    if data_i[3]['sumlevel'] > 1:
        newlevel = data_i[3]['sumlevel'] - 1
        newcontent = master_dic[4][newlevel]
        data_i[3]['sumlevel'] = newlevel
        data_i[3]['content'] = newcontent
    return render_template('homep.html', data_i = data_i)

@app.route("/p5down/", methods=['POST'])
def p5down():
    if data_i[4]['sumlevel'] > 1:
        newlevel = data_i[4]['sumlevel'] - 1
        newcontent = master_dic[5][newlevel]
        data_i[4]['sumlevel'] = newlevel
        data_i[4]['content'] = newcontent
    return render_template('homep.html', data_i = data_i)

if __name__ == '__main__':
    app.run()
