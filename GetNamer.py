class GetNamer:
    def extract_name(self, r, ind):
        link = str(bin(int(r[ind:ind + 4], 16)))[2:]
        link = int(link[2:], 2) * 2
        res, _ = self.get_name(r, link)
        return res

    def get_name(self, r, start_name_index=24):
        name = []

        offset = 0

        while True:
            index = start_name_index + offset

            raw = r[index:index + 4]

            if int(raw, 16) >= 49152:
                link = str(bin(int(raw, 16)))[2:]

                link = int(link[2:], 2) * 2

                rest, offset = get_name(r, link)
                name.append(rest)
                name.append(".")
                break

            length = int(r[index:index + 2], 16)

            if length == 0:
                break

            i = 2
            while i <= length * 2:
                decoded = chr(int(r[index + i:index + i + 2], 16))
                name.append(decoded)
                i += 2

            name.append(".")
            offset += length * 2 + 2

        name = "".join(name[:-1])

        return name, offset