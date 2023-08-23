from dataset.dataset import ThreadDataset, initial_dataset
from dataset.dataset_entries import NetworkKey
from tlv.tlv import TLV

print('creating ds')
ds = ThreadDataset()
ds.set_from_bytes(initial_dataset)

print('creating old tlvs')
old_tlvs = TLV.parse_tlvs(initial_dataset)
print('creating new tlvs')
new_tlvs = [entry.to_tlv() for entry in ds.entries.values()]

print('OLD TLVS:')
for tlv in old_tlvs:
    print(tlv.type, tlv.value)

print()
print('NEW TLVS:')
for tlv in new_tlvs:
    print(tlv.type, tlv.value)
