# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

def writeTree(tokens, node):
    if node is None:
        tokens.append('_')
        return
    tokens.append(str(node.val))
    writeTree(tokens, node.left)
    writeTree(tokens, node.right)

def readTree(tokens, i):
    tok = tokens[i]
    if tok == '_':
        return None, i + 1
    node = TreeNode(int(tok))
    node.left, i = readTree(tokens, i + 1)
    node.right, i = readTree(tokens, i)
    return node, i

class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.
        
        :type root: TreeNode
        :rtype: str
        """
        tokens = []
        writeTree(tokens, root)
        return ' '.join(tokens)

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        
        :type data: str
        :rtype: TreeNode
        """
        tokens = data.split()
        tree, _ = readTree(tokens, 0)
        return tree
        
        

# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))