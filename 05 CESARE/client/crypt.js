// encrypt
Class("Crypt", {
    Crypt: function(text, key) {
        this.text = text;
        this.key = key;
        //dictionary
        this.dic = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"];
    },

    getPos: function(c, key) {
        var pos = this.dic.indexOf(c);
        if ((pos + key) >= this.dic.length) {
            return pos + key - this.dic.length;
        }
        return pos + key;
    },

    encode: function() {
        var result = "";
        for (var i in this.text) {
            var c = this.text[i];
            if ((c == " ") || (c == "\n")) {
                result += c;
            } else {
                result += this.dic[this.getPos(c.toLowerCase(), this.key)];
            }
        }
        return result;
    }
});

// decrypt
Class("Decrypt", {
    Decrypt: function(text, key) {
        this.text = text;
        this.key = key;
        this.dic = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"];
    },

    getPos: function(c, key) {
        var pos = this.dic.indexOf(c);
        if (( pos - key ) >= 0) {
            return pos - key
        }
        return this.dic.length + (pos - key)
    },

    decode: function() {
        var result = "";
        for (var i in this.text) {
            var c = this.text[i];
            if ((c == " ") || (c == "\n")) {
                result += c;
            } else {
                result += this.dic[this.getPos(c.toLowerCase(), this.key)];
            }
        }
        return result;
    }

});